import asyncio
import os
from itertools import cycle

import click
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv


load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


#
# Tasks
#

statuslist = cycle(
    [
        "Pythoning",
        "Doing stuff...",
    ]
)


@tasks.loop(seconds=16)
async def change_status():
    """This is a background task that loops every 16 seconds.
    The coroutine looped with this task will change status over time.
    The statuses used are in the cycle list called `statuslist`_.

    Documentation:
            https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html
    """
    await bot.change_presence(activity=discord.Game(next(statuslist)))
    # Changes the bot status to `Pythoning`_.


async def main():
    async with bot:
        # for filename in os.listdir("./dolores/cogs"):
        #     if filename.endswith(".py"):
        #         # cut off the .py from the file name
        #         await bot.load_extension(f"dolores. cogs.{filename[:-3]}")
        for extension in [
            "dolores.cogs.apple",
            "dolores.cogs.support",
            "dolores.cogs.trello",
        ]:
            await bot.load_extension(extension)

        await bot.start(os.getenv("DISCORD_TOKEN"))


#
# Event handlers
#


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    change_status.start()


#
# CLI
#


@click.group()
def cli():
    pass


@cli.command(name="run")
def run():
    """Runs the bot."""
    asyncio.run(main())
