# bot.py
import os
import discord
import asyncio

from main_uses import *

from dotenv import load_dotenv

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

    userStreaming, wasStreaming = startStreaming, startStreaming
    
    while not client.is_closed():
        uS, wS = await timeChangeLogic(guild, streamHour,
                                       userStreaming, wasStreaming)
        userStreaming, wasStreaming = uS, wS

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

    mContent = message.content
    await checkMessage(guild, message, mContent)

client.loop.create_task(move_task())
client.run(TOKEN)
