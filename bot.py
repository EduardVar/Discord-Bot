# bot.py
import os
import random
import datetime

import discord
import asyncio

from dotenv import load_dotenv
from bot_funcs import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

userStreaming = False
client = discord.Client()

async def move_task():
    await client.wait_until_ready()

    guild = discord.utils.get(client.guilds, name=GUILD)
    streamHour = -1
    
    while not client.is_closed():

        currHour, lastHour = await updateTime()
        
        if not userStreaming:
            currHour, lastHour = await moveNewTime(currHour, lastHour, guild)

            await moveInCategory(currHour, guild)

            await asyncio.sleep(1) # task runs every second

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_member_join(member):
    guild = discord.utils.get(client.guilds, name=GUILD)
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {guild.name}!'
    )

@client.event
async def on_message(message): 
    if message.author == client.user:
        return

    mContent = message.content
    guild = discord.utils.get(client.guilds, name=GUILD)

    if mContent == "~assemble":
        role = discord.utils.get(guild.roles, name="Avengerbots")
        
        response = "{}, Roll Out.".format(role.mention)
        await message.channel.send(response)

    if mContent == "~streaming?":
        voiceChannel = await getHourChannel(currHour, guild)

        for member in voiceChannel.members:
            print(member.name, ":", member.voice.self_stream)


client.loop.create_task(move_task())
client.run(TOKEN)
