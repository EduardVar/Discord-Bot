# bot.py
import os
import random
import datetime

import discord
import asyncio

from dotenv import load_dotenv
from bot_funcs import checkTime, moveInCategory

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

roleID = "<@&675471556926767164>"
now = datetime.datetime.now()
lastHour = now.hour

hourDic = {0:"12 am", 1:"1 am", 2:"2 am", 3:"3 am", 4:"4 am", 5:"5 am",
           6:"6am", 7:"7 am", 8:"8 am", 9:"9 am", 10:"10 am", 11:"11 am",
           12:"12 pm", 13:"1 pm", 14:"2 pm", 15:"3 pm", 16:"4 pm", 17:"5 pm",
           18:"6 pm", 19:"7 pm", 20:"8 pm", 21:"9 pm", 22:"10 pm", 23:"11 pm"}

client = discord.Client()

async def move_task():
    await client.wait_until_ready()
    now = datetime.datetime.now()
    currHour = now.hour
    lastHour = currHour

    guild = discord.utils.get(client.guilds, name=GUILD)
    
    while not client.is_closed():
        lastHour = await checkTime(now, currHour, lastHour, guild)

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


client.loop.create_task(move_task())
client.run(TOKEN)
