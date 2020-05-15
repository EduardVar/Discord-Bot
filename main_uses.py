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

    _, prevHour = await updateTime()
    prevHour = prevHour - 1 if prevHour - 1 >= 0 else 23
    
    vc = await getHourChannel(prevHour, guild)
    startStreaming = False;
    for member in vc.members:
        if member.voice.self_stream:
            startStreaming = True
            streamHour = prevHour

    return streamHour, startStreaming, startStreaming

    
