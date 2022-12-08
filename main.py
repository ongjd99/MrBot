from discord import Client, Embed, Color
import discord
from replit import db
from discord.utils import get as dcget
import os
import asyncio
import requests

client = Client()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run(os.environ['TOKEN'])
