import datetime
import discord

hourDic = {0:"12 am", 1:"1 am", 2:"2 am", 3:"3 am", 4:"4 am", 5:"5 am",
           6:"6am", 7:"7 am", 8:"8 am", 9:"9 am", 10:"10 am", 11:"11 am",
           12:"12 pm", 13:"1 pm", 14:"2 pm", 15:"3 pm", 16:"4 pm", 17:"5 pm",
           18:"6 pm", 19:"7 pm", 20:"8 pm", 21:"9 pm", 22:"10 pm", 23:"11 pm"}

now = datetime.datetime.now()
currHour = now.hour
lastHour = currHour

async def checkTime(now, currHour, lastHour, guild):
    now = datetime.datetime.now()
    currHour = now.hour

    if currHour != lastHour:
        # Write code here to move people
        print("It is now", hourDic[currHour])
        voiceChannel = discord.utils.get(guild.voice_channels,
                                         name=hourDic[lastHour])
        destination = discord.utils.get(guild.voice_channels,
                                         name=hourDic[currHour])

        for member in voiceChannel.members:
            await member.move_to(destination)

    # Will update lastHour if currHour has changed
    lastHour = currHour
    return currHour

async def moveInCategory(currHour, guild):
    # Category move
    timeCategory = discord.utils.get(guild.categories, name="Times")
    vcs = timeCategory.voice_channels

    for channel in vcs:
        for member in channel.members:
            if channel.name != hourDic[currHour]:
                destination = discord.utils.get(guild.voice_channels,
                                                name=hourDic[currHour])
                await member.move_to(destination)

                    
