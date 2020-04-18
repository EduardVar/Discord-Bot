# bot.py
import os
import random

import discord
import asyncio

import datetime

from dotenv import load_dotenv

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

async def my_background_task():
    await client.wait_until_ready()
    now = datetime.datetime.now()
    currHour = now.hour
    lastHour = currHour
    
    while not client.is_closed():
        now = datetime.datetime.now()
        currHour = now.hour

        if currHour != lastHour:
            # Write code here to move people
            print("THE HOUR HAS CHANGED")
            guild = discord.utils.get(client.guilds, name=GUILD)
            voiceChannel = discord.utils.get(guild.voice_channels,
                                         name=hourDic[lastHour])
            destination = discord.utils.get(guild.voice_channels,
                                         name=hourDic[currHour])

            for member in voiceChannel.members:
                await member.move_to(destination)

            lastHour = currHour
        else:
            print("LOOP")
            print("Second: " + str(now.second))
            print("Hour: " + str(now.hour))

        await asyncio.sleep(5) # task runs every 5 seconds

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    #for r in guild.roles:
        #print(r)

    print(hourDic[now.hour])


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
        
    elif '~closed?' in mContent.lower():
        print(not client.is_closed())

    elif mContent == 'raise-exception':
        raise discord.DiscordException

    elif mContent == '~users':
        voiceChannel = discord.utils.get(guild.voice_channels,
                                         name=hourDic[now.hour])

        for member in voiceChannel.members:
            await message.channel.send(member);

    elif mContent == "~move":
        voiceChannel = discord.utils.get(guild.voice_channels,
                                         name="General")
        destination = discord.utils.get(guild.voice_channels,
                                     name="School")

        for member in voiceChannel.members:
            await member.move_to(destination)

client.loop.create_task(my_background_task())
client.run(TOKEN)
