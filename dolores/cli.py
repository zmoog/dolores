import datetime
import json
import os
from itertools import cycle

import click
import discord
import httpx
from discord.ext import commands, tasks
from dotenv import load_dotenv

from .commands import ping, iphones


load_dotenv()


# @tasks.loop(seconds=5)
# async def my_background_task():
#     # Your code here
#     print("Running a task every 5 seconds")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

#
# commands
#

bot.add_command(ping)
bot.add_command(iphones)


#
# Tasks
#

statuslist = cycle([
		'Pythoning',
		'Doing stuff...',
	])

@tasks.loop(seconds=16)
async def change_status():
	"""This is a background task that loops every 16 seconds.
	The coroutine looped with this task will change status over time.
	The statuses used are in the cycle list called `statuslist`_.
	
	Documentation:
		https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html
	"""
	await bot.change_presence(activity=discord.Game(next(statuslist)))
	#Changes the bot status to `Pythoning`_.


# utc = datetime.timezone.utc
# 
# # If no tzinfo is given then UTC is assumed.
# times = [
#     datetime.time(hour=8, tzinfo=utc),
#     datetime.time(hour=12, minute=30, tzinfo=utc),
#     datetime.time(hour=16, minute=40, second=30, tzinfo=utc)
# ]
# 
# class MyCog(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         self.my_task.start()
# 
#     def cog_unload(self):
#         self.my_task.cancel()
# 
#     @tasks.loop(time=times)
#     async def my_task(self):
#         print("My task is running!")


#
# Event handlers
#

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
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
    bot.run(os.getenv("DISCORD_TOKEN"))
