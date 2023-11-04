import datetime

from discord.ext import commands, tasks


utc = datetime.timezone.utc

# If no tzinfo is given then UTC is assumed.
times = [
    # datetime.time(hour=8, tzinfo=utc),
    # datetime.time(hour=16, minute=40, second=30, tzinfo=utc)
    datetime.time(hour=15, minute=39, tzinfo=utc),
]


class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.my_task.start()
        print("SupportCog has been loaded!")

    #
    # Lifecycle
    #

    def cog_unload(self):
        self.my_task.cancel()
        print("SupportCog has been unloaded!")

    #
    # Periodic tasks (loops)
    #

    @tasks.loop(time=times)
    async def my_task(self):
        print("SupportCog is running!")

    #
    # Commands
    #

    @commands.command(name="hey")
    async def hey(self, ctx):
        print("hey")
        await ctx.send("hey")

    @commands.command(name="ping")
    async def ping(self, ctx):
        print("ping")
        await ctx.send("pong")

    @commands.command(name="get_channel")
    async def get_channel(self, ctx, *, given_name=None):
        print("get_channel")
        for channel in ctx.guild.channels:
            if channel.name == given_name:
                wanted_channel_id = channel.id

        await ctx.send(wanted_channel_id)  # this is just to check


async def setup(bot):
    await bot.add_cog(SupportCog(bot))
