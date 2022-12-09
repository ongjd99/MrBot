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

    async def hello():
        await message.channel.send("Hello! It\'s nice to see you!")

    async def thanks():
        await message.add_reaction('\U0000263A')  # smiley
        await channel.send('You are very welcome!')

    async def disable():
        await channel.send('Bye bye :)')
        exit()

    mc = message.content
    channel = message.channel
    author = str(message.author).split('#')[0]  
    if message.author == client.user: return

    parsed_message = mc.split()

    commands = {
        "!hello": hello,
        "!thank you": thanks,
        "!thanks": thanks,
        "!disable": disable,
        "!help": help
    }

    if parsed_message[0] in commands:
        await commands[parsed_message[0]]()

client.run(os.environ['TOKEN'])
