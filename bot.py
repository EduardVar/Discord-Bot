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

    await bot.process_commands(message)


@bot.command(name='assemble', help='--> @ the AvengerBots')
async def assembleCompand(ctx):
    role = discord.utils.get(guild.roles, name="Avengerbots")        
    response = "{}, Roll Out.".format(role.mention)
    await ctx.send(response)

@bot.command(name='games?', help='--> Shows what games people are playing')
async def gamesCommand(ctx):
    response = await showGamesPlayed(guild)                   
    await ctx.send(response)

@bot.command(name='bruh', help='--> You can add a number after bruh to'
             ' repeat the phrase [-400, 400]')
async def bruhCommand(ctx):
    response = await printBruh(ctx.message.content[6:])
    await ctx.send(response)

@bot.command(name='cursed', help='--> Sends an image from r/cursedimages')
async def bruhCommand(ctx):
    response = getImagePost("cursedimages")
    await ctx.send(response)

@bot.command(name='blursed', help='--> Sends an image from r/blusedimages')
async def bruhCommand(ctx):
    response = getImagePost("blursedimages")
    await ctx.send(response)

@bot.command(name='aww', help='--> Sends an image from r/awwnime')
async def bruhCommand(ctx):
    response = getPicLink("awwnime")
    await ctx.send(response)
    

bot.loop.create_task(move_task())
bot.run(TOKEN)
