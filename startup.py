import os, json

print("Enter a command or help")

command = input()
if command == "help":
	print("start - Starts the bot\ntoken [token] - Sets the bot token\nreset - Resets the entire bot\nlimit - Sets a character limit for each person")
	exec(open('startup.py').read())

elif command == "start":
	exec(open('bot.py').read())

elif command.startswith("token"):
	data = {"token": f"{command.split()[1]}", "cogs": ["roleplay", "system"], "fir": True}
	if not os.path.exists("characters/uwu.txt"):
		os.makedirs("characters")
		with open("characters/uwu.json", "w") as f2:
			f2.write("{}")
	with open("data.json", "w") as f1:
		json.dump(data, f1, indent=4)
	exec(open('startup.py').read())

elif command == "reset":
	with open("data.json", "w") as f1:
		data1 = {"token": None}
		json.dump(data1, f1, indent=0)
	with open("config.json", "w") as f2:
		data2 = {"limit": 10}
		json.dump(data2, f2, indent=0)
	for file in os.listdir("characters"):
		for fil in os.listdir(f"characters/{file}"):
			os.remove(fil)
		else:
			os.remove(f"characters/{file}")
	else: 
		os.remove("characters")
		print("Bot reset")
		exec(open('startup.py').read())
  
elif command == "limit":
	with open("config.json", "w") as f:
		try: 
			limit = int(command.split()[1])
		except IndexError:
			limit = 10
		finally:
			print(f"Limit set to {limit}")
			data = {"limit": limit}
			with open("config.json") as f:
				json.dump(data, f, indent=0)

else: 
	print("Unknown command")
	exec(open('startup.py').read())
