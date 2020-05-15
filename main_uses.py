import discord

from funcs.playing_games import showGamesPlayed
from funcs.misc_commands import *
from scrapers.reddit_post import *

from funcs.time_and_move import *

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


async def setupMoveTask(guild):
    streamHour = -1
    startStreaming = False
    
    timeCategory = discord.utils.get(guild.categories, name="Times")
    vcs = timeCategory.voice_channels
    
    for channel in vcs:
        for member in channel.members:
            if member.voice.self_stream:
                streamHour = await getTimeFromChannel(channel)
                startStreaming = True

    return streamHour, startStreaming, startStreaming

    
