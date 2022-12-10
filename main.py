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
            em.add_field(name="\nModeration Tools",
                         value="disable",
                         inline=False)
            em.add_field(
                name="\nMiscellaneous Tools",
                value="hello\nthanks",
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
                     "`[question]` - Anything the user inputs (although makes more sense to be a question)", "N/A"],
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

    mc = message.content
    channel = message.channel
    author = str(message.author).split('#')[0]  
    if message.author == client.user: return

    parsed_message = mc.split()

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
        "!restricted": restricted
    }

    if parsed_message[0] in commands:
        await commands[parsed_message[0]]()

client.run(os.environ['TOKEN'])
