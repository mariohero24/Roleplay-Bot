import discord, json, os
from aiohttp import ClientSession
from discord.ext import commands
from customdefs.colours import blank
description=""
class Roleplay(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@discord.slash_command(description="Creates a character")
	async def create(self, ctx: discord.ApplicationContext, image: discord.Option(discord.Attachment, description="Attachment to set as profile picture of your character"), name: discord.Option(str, description="Name of your character")):
		with open("config.json") as f1:
			data1 = json.load(f1)
			if not os.path.exists(f"characters/{ctx.author.id}"):
				os.makedirs(f"characters/{ctx.author.id}")
			if not len(os.listdir(f"characters/{ctx.author.id}")) >= data1['limit']:
				with open(f"characters/{ctx.author.id}/{name}.json", "w") as f2:
					data2 = {
						"name": name, "image": image.url
					}
					json.dump(data2, f2, indent=4)
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


	@discord.slash_command(description="Lists all the characters you have")
	async def characters(self, ctx: discord.ApplicationContext):
		embed = discord.Embed(colour=blank)
		for dir in os.listdir(f"characters/{ctx.author.id}"):
			with open(f"characters/{ctx.author.id}/{dir}") as f:
				data = json.load(f)
				embed.add_field(name=data['name'], value=data['image'])
		if len(os.listdir(f"characters/{ctx.author.id}")) <= 6:
			await ctx.respond(embed=embed)


def setup(bot):
	bot.add_cog(Roleplay(bot))