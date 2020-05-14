# bot.py
import os
import discord
import asyncio

from main_uses import *

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('CLIENT_SECRET')
AGENT = os.getenv('USER_AGENT')

bot = commands.Bot(command_prefix='~')
guild = discord.guild.Guild
initPraw(ID, SECRET, AGENT)

async def move_task():
    await bot.wait_until_ready()

    global guild
    guild = discord.utils.get(bot.guilds, name=GUILD)
    streamHour, userStreaming, wasStreaming = await setupMoveTask(guild)
    
    while not bot.is_closed():
        uS, wS = await timeChangeLogic(guild, streamHour,
                                       userStreaming, wasStreaming)
        userStreaming, wasStreaming = uS, wS

        await asyncio.sleep(1) # task runs every second

@bot.event
async def on_ready():
    global guild
    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@bot.event
async def on_member_join(member):
    global guild
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to {guild.name}!'
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await checkMessage(guild, message, message.content)
    await bot.process_commands(message)

# Won't run while on_message is a thing (will have to test)
@bot.command(name='tester', help='Trying to see if help works with test too!')
async def testerCommand(ctx):
    response = "It's working"
    await ctx.send(response)

bot.loop.create_task(move_task())
bot.run(TOKEN)
