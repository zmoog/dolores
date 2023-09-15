import json

import discord
import httpx
from discord.ext import commands


@commands.command()
async def ping(ctx):
	await ctx.send('pong')

@commands.command()
async def iphones(ctx, name: str = 'iPhone 13 Pro Max'):
	async with httpx.AsyncClient() as session:
		r = await session.get('https://raw.githubusercontent.com/zmoog/refurbished-history/main/stores/it/iphones.json')
		if r.status_code == 200:
			all_iphones = json.loads(r.text)

			filtered_iphones = list(filter(lambda x: name in x['name'], all_iphones))

			msg = ''
			for iphone in filtered_iphones[:5]:
				msg += f'- [{iphone["name"]}]({iphone["url"]}) — {iphone["price"]}\n'

			print(msg)

			await ctx.send(msg)
