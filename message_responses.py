import discord

from funcs.playing_games import showGamesPlayed
from funcs.misc_commands import *
from scrapers.reddit_post import *

async def checkMessage(guild, message, mContent):
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
