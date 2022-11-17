import discord, json, os
from discord.ext import commands
from customdefs import colours

description=""

class Roleplay(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@discord.slash_command(description="Creates a character")
	async def create(self, ctx: discord.ApplicationContext, image: discord.Option(discord.Attachment, description="Attachment to set as profile picture of your character"), name: discord.Option(str, description="Name of your character"), description: discord.Option(str, description="Description of your character")="No description"):
		with open("config.json") as f1:
			data1 = json.load(f1)
			if not os.path.exists(f"characters/{ctx.author.id}"):
				os.makedirs(f"characters/{ctx.author.id}")
			if not len(os.listdir(f"characters/{ctx.author.id}")) >= data1['limit']:
				with open(f"characters/{ctx.author.id}/{name}.json", "w") as f2:
					data2 = {
						"name": name, "image": image.url, "description": description
					}
					json.dump(data2, f2, indent=4)
				webhook = await ctx.channel.create_webhook(name="CHARACTERHOOK")
				await webhook.send("Hello.", username=name, avatar_url=image.url)
				await ctx.respond("Done", ephemeral=True)
				await webhook.delete()


	@discord.slash_command(description="Sends a message as your character")
	async def send(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character"), message: discord.Option(str, description="Message to send as your character")):
		if os.path.exists(f"characters/{ctx.author.id}/{character}.json"):
			with open(f"characters/{ctx.author.id}/{character}.json") as f1:
				data1 = json.load(f1)
				character = await ctx.channel.create_webhook(name="CHARACTERHOOK")
				await character.send(message, username=data1['name'], avatar_url=data1['image'])
				await ctx.respond("Sent", ephemeral=True)
				await character.delete()

	
	@discord.slash_command(description="Deletes a character")
	async def delete(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of the character")):
		os.remove(f"characters/{ctx.author.id}/{character}.json")
		await ctx.respond("Done", ephemeral=True)


	@discord.slash_command(description="Lists all the characters you have")
	async def characters(self, ctx: discord.ApplicationContext):
		embed = discord.Embed(colour=colours.none)
		for dir in os.listdir(f"characters/{ctx.author.id}"):
			with open(f"characters/{ctx.author.id}/{dir}") as f:
				data = json.load(f)
				embed.add_field(name=data['name'], value=data['description'])
		await ctx.respond(embed=embed)


	@discord.slash_command(description="Shows a character")
	async def show(self, ctx: discord.ApplicationContext, character: discord.Option(str, description="Name of character")):
		with open(f"characters/{ctx.author.id}/{character}.json") as f:
			data = json.load(f)
			embed = discord.Embed(title=data['name'], colour=colours.none, description=data['description'])
			embed.set_thumbnail(url=data['image'])
		await ctx.respond(embed=embed)


	@discord.slash_command(description="Edit a character")
	async def edit(self, ctx: discord.ApplicationContext, oldname: discord.Option(str, description="Name of character you want to edit"), newname: discord.Option(str, description="New name for your character")=None, image: discord.Option(discord.Attachment, description="New attachment to set as profile picture of your character")=None, description: discord.Option(str, description="New description for your character")=None):
		with open(f"characters/{ctx.author.id}/{oldname}.json") as f1:
			data = json.load(f1)
			if newname == None:
				newname = oldname
			if image == None:
				img = data['image']
			else:
				img = image.url
			if description == None:
				desc = data['description']
			else:
				desc = description
			embed = discord.Embed(title=newname, colour=colours.none, description=data)
			embed.set_thumbnail(url=image.url)
			data2 = {"name": newname, "description": desc, "image": img}
			os.remove(f"characters/{ctx.author.id}/{oldname}.json")
			with open(f"characters/{ctx.author.id}/{newname}.json", "w") as f2:
				json.dump(data2, f2, indent=4)
		await ctx.respond(embed=embed)


def setup(bot):
	bot.add_cog(Roleplay(bot))