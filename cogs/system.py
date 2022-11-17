import discord, json, os
from discord.ext import commands

class SYS(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.Cog.listener('on_ready')
	async def ready(self):
		print("Online")
		with open("data.json") as f1:
			data = json.load(f1)
			fir = data['fir']
			if fir == True:
				os.remove("characters/uwu.json")
				print(f"https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=536887296&scope=bot%20applications.commands")
		with open("data.json", "w") as f2:
			data2 = {
				"token": data['token'], "cogs": data['cogs'], "fir": False
			}
			json.dump(data2, f2, indent=4)
   

	@commands.Cog.listener('on_application_command_error')
	async def apperror(self, ctx: discord.ApplicationContext, error):
		if isinstance(error, commands.BotMissingPermissions):
			await ctx.respond("The bot does not have permissions to use this command. Missing permissions:\n" + "\n".join(
				[
					str(p[0]).replace("_", " ").title()
					for p in error.missing_permissions
					if p[1]
				]
			))
		else:
			with open("errors.txt", "a") as f:
				f.write(f"{error}\n")


def setup(bot):
	bot.add_cog(SYS(bot))