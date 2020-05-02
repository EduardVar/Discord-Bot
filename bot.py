# bot.py
import os
import random
import datetime

import discord
import asyncio

from dotenv import load_dotenv
from funcs.time_and_move import *
from funcs.playing_games import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
guild = discord.guild.Guild

async def move_task():
    await client.wait_until_ready()

    global guild
    guild = discord.utils.get(client.guilds, name=GUILD)
    streamHour = -1

    userStreaming = False
    wasStreaming = False
    
    while not client.is_closed():
        currHour, lastHour = await updateTime()

        a, b, c = await checkIfStreaming(guild, streamHour, wasStreaming)
        userStreaming, streamHour, wasStreaming = a, b, c
        
        if not userStreaming:
            if wasStreaming:
                await moveInCategory(currHour, guild)
                wasStreaming = False
            else:
                currHour, lastHour = await moveNewTime(currHour,
                                                       lastHour, guild)
                await moveInCategory(currHour, guild)            
        else:         
            await moveInCategory(streamHour, guild)
            wasStreaming = True

        await asyncio.sleep(1) # task runs every second

@client.event
async def on_ready():
    global guild
    print(
        f'{client.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_member_join(member):
    global guild
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {guild.name}!'
    )

@client.event
async def on_message(message): 
    if message.author == client.user:
        return

    global guild
    mContent = message.content

    if mContent == "~assemble":
        role = discord.utils.get(guild.roles, name="Avengerbots")        
        response = "{}, Roll Out.".format(role.mention)
        await message.channel.send(response)

    if mContent == "~games?":
        response = await showGamesPlayed(guild)
        await message.channel.send(response)

client.loop.create_task(move_task())
client.run(TOKEN)
