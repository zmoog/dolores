import json
import os
import datetime as dt
import itertools
from typing import Dict

import jinja2
import humanize
from discord.ext import commands, tasks
from trellokit import trello as trellokit


utc = dt.timezone.utc

soon = dt.timedelta(days=3)
upcoming = dt.timedelta(days=7)


class ConfigError(Exception):
    pass


class TrelloCog(commands.Cog):
    """This cog is for Trello boards."""

    def __init__(self, bot, config: Dict[str, Dict[str, Dict[str, str]]]):
        self.bot = bot
        self.config = config

        self.cards = trellokit.Cards(
            api_key=os.environ["TRELLO_KEY"],
            api_token=os.environ["TRELLO_TOKEN"],
        )

        self.remind_due_cards.start()
        print("TrelloCog has been loaded!")

    def cog_unload(self):
        self.remind_due_cards.cancel()
        print("TrelloCog has been unloaded!")

    #
    # Periodic tasks
    #

    @tasks.loop(time=[dt.time(hour=7, minute=45, tzinfo=utc)])
    async def remind_due_cards(self):
        """Remind about due cards."""

        destinations = [
            ("maintenance", "in_progress"),
            ("maintenance", "waiting"),
            ("maintenance", "scheduled"),
        ]

        for board_name, list_name in destinations:
            print(f"reminding about {board_name} {list_name}")
            # Lookup Trello list info.
            cfg = self._find_list_info(board_name, list_name)

            channel = self.bot.get_channel(cfg["channel_id"])

            await self._post_due_cards(channel, board_name, list_name)

    #
    # Commands
    #

    @commands.command("trello-list")
    async def list(
        self, ctx, board_name: str, list_name: str = "in_progress", label: str = None
    ):
        try:
            cfg = self._find_list_info(board_name, list_name)

            cards = self.cards.list(cfg["list_id"], label=label)
            msg = render_cards(card_list_template, cards=cards)

            await ctx.send(msg[:2000])

        except ConfigError as e:
            await ctx.send("Cant find that board or list.")

    @commands.command("trello-due")
    async def due(
        self, ctx, board_name: str, list_name: str = "in_progress", label: str = None
    ):
        """List cards that are due today."""
        await self._post_due_cards(ctx, board_name, list_name, label)

    #
    # Support methods.
    #

    def _find_list_info(self, board_name: str, list_name: str):
        """Finds a list in the config."""

        if board_name not in self.config:
            raise ConfigError(f"Board {board_name} not found.")

        cfg = self.config[board_name]

        if list_name not in cfg:
            raise ConfigError(f"List {list_name} not found.")

        return cfg[list_name]

    async def _post_due_cards(
        self,
        destination,
        board_name: str,
        list_name: str = "in_progress",
        label: str = None,
    ):
        try:
            # Lookup Trello list info.
            cfg = self._find_list_info(board_name, list_name)

            cards = self.cards.list(cfg["list_id"], label=label)
            print(f"found {len(cards)} cards")

            #
            # Group cards by due date bucket.
            #

            now = dt.datetime.now()

            # Filter out cards without due dates and cards that are not due soon.
            cards_due = [
                card
                for card in cards
                if card.due_date and now < card.due_date < now + upcoming
            ]

            # Sort and group cards by due date bucket (overdue, soon, upcoming).
            groups = itertools.groupby(
                sorted(cards_due, key=lambda x: x.due_date), key=bucketize
            )

            print(f"found {len(cards_due)} cards with due dates")

            msg = render_cards(cards_due_template, groups=groups, name=cfg["name"])

            await destination.send(msg[:2000])

        except ConfigError as e:
            await destination.send("Cant find that board or list.")
        except Exception as e:
            print(e)
            await destination.send("Something went wrong.")


#
# Helpers
#


def render_cards(template, **kwargs) -> None:
    try:
        msg = template.render(**kwargs)
    except Exception as e:
        msg = f"Something went wrong: {e}"

    print(msg)
    return msg


def bucketize(card: trellokit.Card):
    """Bucketize cards by due date."""
    now = dt.datetime.now()

    if not card.due_date:
        return None

    if card.due_date < now:
        return "overdue"

    if card.due_date < now + soon:
        return "soon"

    if card.due_date < now + upcoming:
        return "upcoming"

    return "later"


environment = jinja2.Environment()

# Custom Jinja2 filters.
# https://jinja.palletsprojects.com/en/3.0.x/api/#custom-filters
environment.filters["delta_from_now"] = lambda x: dt.datetime.now() - x
environment.filters["naturaldelta"] = humanize.naturaldelta

cards_due_template = environment.from_string(
    """
{% for bucket, items in groups -%}
- {{ bucket|title }}:
  {% for card in items -%}
  - [{{ card.name }}]({{ card.url }}) — {{ card.due_date|delta_from_now|naturaldelta }}
  {% endfor %}
{% else %}
✅ There are no cards with due dates in the list **{{ name }}**.
{% endfor %}
"""
)

card_list_template = environment.from_string(
    """Here are the cards for board:
{% for labels, items in cards|groupby("labels") -%}
- {{ labels|join(", ") }}:
  {% for card in items -%}
  - [{{ card.name }}]({{ card.url }}) — {{ card.age }}
  {% endfor %}
{% endfor %}

"""
)


async def setup(bot):
    # load config from trello.config.json file.
    with open("trello.config.json", "r") as f:
        config = json.load(f)
        await bot.add_cog(TrelloCog(bot, config))
