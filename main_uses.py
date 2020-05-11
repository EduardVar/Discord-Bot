import discord

from funcs.playing_games import showGamesPlayed
from funcs.misc_commands import *
from scrapers.reddit_post import *

from funcs.time_and_move import *

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


async def timeChangeLogic(guild, streamHour, userStreaming, wasStreaming):
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

    return userStreaming, wasStreaming
