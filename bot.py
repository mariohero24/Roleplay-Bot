import discord, json
from discord.ext import commands


with open("data.json") as f:
	data = json.load(f)
	token = data['token']

bot = discord.Bot(intents=discord.Intents.default())



if token == None:
	print("There is no token set.")
else:
	extensions = data['cogs']
	for extension in extensions:
		bot.load_extension(f"cogs.{extension}")
	bot.run(token)