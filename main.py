#########################################
# main.py
#########################################
# Ver 1.0
# Last edited: 1/11/2022
#########################################

import discord
from discord.ext import commands
from music import Player
from quotes import Frases
import os
from keepalive import keep_alive
import requests

intents = discord.Intents.default()
intents.members=True

client = commands.Bot(command_prefix="#", intents = intents)

@client.event
async def on_ready():
  print("Tamo activos, tamo redi")

client.add_cog(Player(client))
client.add_cog(Frases(client))

keep_alive()
client.run(os.getenv('treasure'))
