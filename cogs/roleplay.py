import discord, json, os
from aiohttp import ClientSession
from discord.ext import commands
description=""
class Roleplay(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@discord.slash_command(description="Creates a character")
	async def create(self, ctx: discord.ApplicationContext, image: discord.Option(discord.Attachment, description="Attachment to set as profile picture of your character"), name: discord.Option(str, description="Name of your character")):
		data = {
			"name": name, "image": image.url
		}
		if not os.path.exists(f"characters/{ctx.author.id}"):
			os.makedirs(f"characters/{ctx.author.id}")
		with open(f"characters/{ctx.author.id}/{name}.json", "w") as f:
			json.dump(data, f, indent=4)
		webhook = await ctx.channel.create_webhook(name="CHARACTERHOOK")
		await webhook.send("Hello.", username=name, avatar_url=image.url)
		await ctx.respond("Done", ephemeral=True)
		await webhook.delete()


	@discord.slash_command(description="Sends a message as your character")
	async def send(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character"), message: discord.Option(str, description="Message to send as your character")):
		if os.path.exists(f"characters/{ctx.author.id}/{character}.json"):
			with open(f"characters/{ctx.author.id}/{character}.json") as f:
				data = json.load(f)
				character = await ctx.channel.create_webhook(name="CHARACTERHOOK")
				await character.send(message, username=data['name'], avatar_url=data['image'])
				await ctx.respond("Sent", ephemeral=True)
				await character.delete()
	
	
	@discord.slash_command(description="Deletes a character")
	async def delete(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character")):
		os.remove(f"characters/{ctx.author.id}/{character}.json")
		await ctx.respond("Done", ephemeral=True)


def setup(bot):
	bot.add_cog(Roleplay(bot))