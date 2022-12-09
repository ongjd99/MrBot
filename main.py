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
        "!disable": disable
    }

    if parsed_message[0] in commands:
        await commands[parsed_message[0]]()

client.run(os.environ['TOKEN'])
