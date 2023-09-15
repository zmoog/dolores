import json

import discord
import httpx
from discord.ext import commands

# The discord.ext.commands framework docs are available at:
# https://discordpy.readthedocs.io/en/stable/ext/commands/commands.html
#
# The Discord docs for message formatting:
# Markdown Text 101 (Chat Formatting: Bold, Italic, Underline) 
# https://support.discord.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline


@commands.command()
async def ping(ctx):
	await ctx.send('pong')

@commands.command()
async def iphones(ctx, name: str = '13 Pro Max'):
	"""This command will send a list of refurbished iPhones from the Apple Store."""
	async with httpx.AsyncClient() as session:
		r = await session.get('https://raw.githubusercontent.com/zmoog/refurbished-history/main/stores/it/iphones.json')
		if r.status_code != 200:
			await ctx.send(f'Something went wrong (http status f{r.status_code}).')
			print(r.text)
			return

		all_iphones = json.loads(r.text)

		filtered_iphones = list(filter(lambda x: name in x['name'], all_iphones))
		if len(filtered_iphones) == 0:
			await ctx.send(f'No iPhones found with "{name}" in the name.')
			return

		msg = f'Here are the latest iPhones {name}:\n'
		for iphone in filtered_iphones[:10]:
			msg += f'- [{iphone["name"]}]({iphone["url"]}) — {iphone["price"]} (-{iphone["savings_price"]})\n'

		print(msg)

		await ctx.send(msg)
