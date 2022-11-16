import os, json

print("Enter a command or help")

standard_input="start"

command = input()
if command == "help":
	print("start - Starts the bot\ntoken [token] - Sets the bot token\nreset - Resets the entire bot")
	exec(open('startup.py').read())

elif command == "start":
	exec(open('bot.py').read())

elif command.startswith("token"):
	data = {"token": f"{command.split()[1]}", "cogs": ["roleplay", "system"], "fir": True}
	os.makedirs("characters/uwu")
	with open("data.json", "w") as f:
		json.dump(data, f, indent=4)
	exec(open('startup.py').read())

elif command == "reset":
	data = {"token": None}
	with open("data.json", "w") as f:
		json.dump(data, f, indent=0)
	for file in os.listdir("characters"):
		for fil in os.listdir(f"characters/{file}"):
			os.remove(fil)
		else:
			os.remove(f"characters/{file}")
	else: 
		exec(open('startup.py').read())

else: 
	print("Unknown command")
	exec(open('startup.py').read())