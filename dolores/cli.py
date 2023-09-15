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
