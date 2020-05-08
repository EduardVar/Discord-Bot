# bot.py
import os
import random
import datetime

import discord
import asyncio

from dotenv import load_dotenv
from funcs.time_and_move import *
from funcs.playing_games import showGamesPlayed
from funcs.misc_commands import *

from scrapers.reddit_post import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('CLIENT_SECRET')
AGENT = os.getenv('USER_AGENT')

client = discord.Client()
guild = discord.guild.Guild

initPraw(ID, SECRET, AGENT)

async def move_task():
    await client.wait_until_ready()

    global guild
    guild = discord.utils.get(client.guilds, name=GUILD)
    streamHour = -1

    _, prevHour = await updateTime()
    prevHour = prevHour - 1 if prevHour - 1 >= 0 else 23
    
    vc = await getHourChannel(prevHour, guild)
    startStreaming = False;
    for member in vc.members:
        if member.voice.self_stream:
            startStreaming = True
            streamHour = prevHour

    userStreaming = startStreaming
    wasStreaming = startStreaming
    
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

    elif mContent == "~games?":
        response = await showGamesPlayed(guild)                   
        await message.channel.send(response)

    elif "~bruh" in mContent[0:5]:
        response = await printBruh(mContent[6:])
        await message.channel.send(response)

    elif mContent == "~cursed":
        response = getImagePost("cursedimages")
        await message.channel.send(response)

    elif mContent == "~blursed":
        response = getImagePost("blursedimages")
        await message.channel.send(response)

    elif mContent == "~aww":
        response = getPicLink("awwnime")
        await message.channel.send(response)

client.loop.create_task(move_task())
client.run(TOKEN)
