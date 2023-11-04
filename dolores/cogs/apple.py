import datetime
import json

from discord.ext import commands, tasks
import httpx

utc = datetime.timezone.utc

# If no tzinfo is given then UTC is assumed.
times = [
    # datetime.time(hour=8, tzinfo=utc),
    # datetime.time(hour=16, minute=40, second=30, tzinfo=utc)
    datetime.time(hour=15, minute=39, tzinfo=utc),
]


class AppleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("AppleCog has been loaded!")

    #
    # Lifecycle
    #

    def cog_unload(self):
        print("AppleCog has been unloaded!")

    #
    # Commands
    #

    @commands.command(name="iphones")
    async def lookup_iphones(self, ctx, *, given_name: str = "13 Pro Max"):
        """This command will send a list of refurbished iPhones from the Apple Store."""
        print("lookup_iphones")
        try:
            await self._lookup_products(ctx, "iphones", given_name)
        except Exception as e:
            print(e)

    @commands.command(name="macs")
    async def lookup_macs(self, ctx, *, given_name: str = "MacBook Pro"):
        """This command will send a list of refurbished Macs from the Apple Store."""
        print("lookup_macs")
        try:
            await self._lookup_products(ctx, "macs", given_name)
        except Exception as e:
            print(e)

    async def _lookup_products(self, ctx, product_family, given_name):
        print("lookup_products")
        async with httpx.AsyncClient() as session:
            r = await session.get(
                f"https://raw.githubusercontent.com/zmoog/refurbished-history/main/stores/it/{product_family}.json"
            )
            if r.status_code != 200:
                await ctx.send(f"Something went wrong (http status f{r.status_code}).")
                print(r.text)
                return

            all_products = json.loads(r.text)

            filtered_products = list(
                filter(lambda x: given_name in x["name"], all_products)
            )
            if len(filtered_products) == 0:
                await ctx.send(f'No iPhones found with "{given_name}" in the name.')
                return

            msg = f"Here are the latest Macs {given_name}:\n"
            for product in filtered_products[:10]:
                msg += f'- [{product["name"]}]({product["url"]}) — {product["price"]} (-{product["savings_price"]})\n'

            print(msg)

            await ctx.send(msg[:2000])


async def setup(bot):
    await bot.add_cog(AppleCog(bot))
