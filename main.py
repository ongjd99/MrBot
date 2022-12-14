from discord import Client, Embed, Color
import discord
from replit import db
from discord.utils import get as dcget
import os
import asyncio
import requests
import random

client = Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    async def help():
        # !help
        if len(parsed_message) == 1:
            em = discord.Embed(
                title="__**Help**__",
                description=
                "Use `!help [command]`for extended information on a command.",
                color=0xADD8E6,
                inline=False)
            em.add_field(
                name ="Fun Tools", 
                value = "8ball", 
                inline = False)
            em.add_field(
                name="\nModeration Tools",
                value="restricted\ndisable",
                inline=False)
            em.add_field(
                name="\nMiscellaneous Tools",
                value="hello\nthanks\nremind\ntranslate",
                inline=False)
            await message.channel.send(embed=em)
            return
        # !help [command]
        else:
            description = "Command does not exist."
            message_array = mc.split(' ')
            command = " ".join(message_array[1:])
            # Dictionary of Command, Key = "command name", Value = ["quick decsription", "long description", "arguments", "assocaited commands"]
            # `text` highlights code in Discord chat
            commands = {
                "disable": [
                    " - Shuts Mr Bot down.",
                    "Displays a simple goodbye message to the channel and shuts down",
                    "N/A", "N/A"
                ],
                "hello": [
                    " - Displays a hello message.",
                    "Displays a simple hello message in the channel.", "N/A",
                    "N/A"
                ],
                "thanks": [
                    " - Displays a message of gratitude.",
                    "Displays a simple response from our bot to the channel. Use when you want to say thank you to Gonzo. :)",
                    "N/A", "N/A"
                ],
                "8ball": [
                    " `[question]` Ask the magic 8 ball a question and get a response.", 
                    "Ask the magic 8 ball a question (or anything else) and get a response from a list of possible responses",
                     "`[question]` - Anything the user inputs (although makes more sense to be a question)", "N/A"
                ],
                "restricted": [
                    " - A moderation tool to create restricted words.",
                    "Using the associated commands, admins can create a list of restricted words. Whenever a user sends a message, the message is parsed for any restricted words and if detected, the message is deleted and a warning is displayed.", 
                    "N/A", 
                    "!restricted list\n!restricted add `[word]`\n!restricted delete `[index]`"
                ],
                "restricted list": [
                    " - Displays the list of restricted words.", 
                    "Displays the list of restricted words of the server with associated index. If a restricted word is said by any user, that message is deleted and a warning is issued.", 
                    "N/A", 
                    "!restricted"
                ],
                "restricted add": [
                    " `[word]` - Adds a word to the list of restricted words.", 
                    "Adds a word to the list of restricted words. If a user says a restricted word, that message is deleted and a warning is issued.", 
                    "`[word]` - any word (or number technically)", 
                    "!restricted"
                ],
                "restricted delete": [
                    " `[index]` -  Deletes a word from the list of restricted words.", 
                    "Deletes a word from the list of restricted words by using the associating index. To find the index of a specific word, call `!restricted list` first.", 
                    "`[index]` - Valid index", 
                    "!restricted"
                ],
                "remind" : [
                    "`[amount of time and unit] [reminder]` - Reminds the user to do something.", 
                    "Displays a confirmation mention of the reminder to the channel. After the given time, the user is mentioned and reminded of their given reminder.", 
                    "`[amount_of_time_and_unit]` - any positive integer value with one of the following units of time: [s, m, h, d] trailing behind with no space delimiter\n`[reminder]` - a task or goal or something to be reminded about",
                    "N/A"],
                "translate": [
                    "`[message]` - Displays the Spanish translation of an English message.", 
                    "Displays the Spanish translation of a message of an English message.", 
                    "`[message]` - an english phrase", 
                    "N/A"],
            }
            if command in commands:
                info = commands[command]
                description = info[0]
                em = discord.Embed(title="__**!{}**__{}".format(
                    command, description),
                                   color=0xADD8E6)
                em.add_field(name="Description", value=info[1], inline=False)
                em.add_field(name="Argument(s)", value=info[2], inline=False)
                em.add_field(name="Associated Commands",
                             value=info[3],
                             inline=False)
            else:
                em = discord.Embed(title="__**!{}**__ - {}".format(
                    command, description),
                                   color=0xADD8E6)
            await message.channel.send(embed=em)

    async def restricted():
        #!restricted (and no other command passed)
        if len(parsed_message) == 1:
            await message.channel.send("Please refer to !help restricted for further instructions")
        
        #!restricted list
        if parsed_message[1] == "list":
            try:
                i = 1
                list_of_words = []
                for each in db["restricted"]:
                    list_of_words.append("\n{}. ||{}||".format(i, each))
                i += 1
                if len(list_of_words) == 0:
                    list_of_words.append("There's nothing here")
                restricted_list = Embed(title="List of Restricted Words. May contain offensive language", description="".join(list_of_words), color=0x008080)
                await message.channel.send(embed=restricted_list)
            except:
                await message.channel.send("There are currently no restricted words")

        #!restricted add
        elif parsed_message[1] == "add":
            if "restricted" not in db:
                db["restricted"] = [parsed_message[2]]
            if parsed_message[2] in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'}:
                await message.channel.send("You cannot ban single digit numbers *(as a safety precaution)*")
                return
            try:
                await message.delete()
                db["restricted"].append(parsed_message[2])
                await message.channel.send("Added the word: ||{}||".format(parsed_message[2]))
            except:
                await message.channel.send("Something didn't work right. Check the word you are adding and try again.")

        #!restricted delete
        elif parsed_message[1] == "delete":
            index = int(parsed_message[2]) - 1
            if index > len(db["restricted"]) or index < 0:
                await message.channel.send("You've inputted an invalid index")
            else:
                new_restricted_list = db["restricted"]
                await message.channel.send("Successfully deleted the word ||{}||".format(new_restricted_list[index]))
                del new_restricted_list[index]
                db["restricted"] = new_restricted_list

        #!restricted (aka there's no associated command passed)
        else:
            await message.channel.send("Please refer to !help restricted for further instructions.")

    async def restrictedWordFound():
        await message.delete()
        await message.channel.send("Uh oh! Someone said a banned word!")
        warning = Embed(title = "@{}".format(message.author), description = "||{}||".format(message.content), color = 0x008080)
        await message.channel.send(embed=warning)

    async def remind():
        def convert(time):
            # seconds, minutes, hours, or days
            time_units = ['s', 'm', 'h', 'd']
            # Values in seconds
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600*24}
            unit = time[-1]
            if unit not in time_units:
                return -1
            try:
                amount = int(time[:-1])
            except:
                return -2
            # Amount of time in seconds
            return amount * time_dict[unit]

        if len(parsed_message) <= 2:
            await message.channel.send("**Warning**: Arguments were not entered corrently. Please use `!help remind` for more information.")
            return
        time = (parsed_message[1])
        reminder = " ".join(parsed_message[2:])
        converted_time = convert(time)
        if converted_time < 0:
            await message.channel.send("**Warning**: Time was not entered corrently. Please use `!help remind` for more information.")
            return
        await message.channel.send(f"I'll remind you to **{reminder}** in **{time}**.")
        await asyncio.sleep(converted_time)
        await message.channel.send(f"{message.author.mention} Remember to **{reminder}**!")

    async def hello():
        await message.channel.send("Hello! It\'s nice to see you!")

    async def thanks():
        await message.add_reaction('\U0000263A')  # smiley
        await channel.send('You are very welcome!')

    async def disable():
        await channel.send('Bye bye :)')
        exit()

    async def eight_ball():
        if len(parsed_message) == 1:
            await message.channel.send("You didn't ask a question")
            return
        eight_ball_responses = ["Yes", "No", "Definitely", "Signs point to yes", "Better not tell you now", "It is doubtful", "Do not rely on it"]
        await message.channel.send(random.choice(eight_ball_responses))

    async def translate():
        message_array = mc.split(' ')
        source_text = " ".join(message_array[1:])
        target_data = requests.post('https://translate.argosopentech.com/translate', data={'q':source_text, 'source':'en', 'target':'es'})
        if target_data.status_code == 200:
            target_text = target_data.json()
            await message.channel.send(target_text["translatedText"].capitalize())
        else:
            print("Sorry, we couln't translate your message.")

    mc = message.content
    channel = message.channel
    if message.author == client.user: return

    parsed_message = mc.split()
    if "restricted" in db:
        for each in parsed_message:
            if each in db["restricted"]:
                await restrictedWordFound()
                return

    commands = {
        "!hello": hello,
        "!thank you": thanks,
        "!thanks": thanks,
        "!disable": disable,
        "!help": help,
        "!8ball": eight_ball,
        "!restricted": restricted,
        "!remind": remind,
        "!translate": translate
    }

    if parsed_message[0] in commands:
        await commands[parsed_message[0]]()

client.run(os.environ['TOKEN'])
