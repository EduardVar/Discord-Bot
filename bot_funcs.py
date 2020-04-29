import datetime
import discord

hourDic = {0:"12 am", 1:"1 am", 2:"2 am", 3:"3 am", 4:"4 am", 5:"5 am",
           6:"6am", 7:"7 am", 8:"8 am", 9:"9 am", 10:"10 am", 11:"11 am",
           12:"12 pm", 13:"1 pm", 14:"2 pm", 15:"3 pm", 16:"4 pm", 17:"5 pm",
           18:"6 pm", 19:"7 pm", 20:"8 pm", 21:"9 pm", 22:"10 pm", 23:"11 pm"}

now = datetime.datetime.now()
currHour = now.hour
lastHour = currHour


async def updateTime():
    global currHour
    global lastHour
    
    lastHour = currHour
    
    now = datetime.datetime.now()
    currHour = now.hour

    return currHour, lastHour


async def checkIfStreaming(guild, streamHour, wasStreaming):
    global lastHour

    streaming = False

    if not wasStreaming:
        streamHour = lastHour
    
    if currHour != streamHour:
        voiceChannel = await getHourChannel(streamHour, guild) #lastHour
        textChannel = discord.utils.get(guild.text_channels, name="general")

        for member in voiceChannel.members:
            if member.voice.self_stream:
                streaming = True

                if not wasStreaming:
                    response = ("{}, you're still streaming; when there are no "
                                "streams left in your voice channel, I'll move "
                                "everyone to the "
                                "correct channel.").format(member.mention)
                    await textChannel.send(response)

        # Updates lastHour to currHour
        lastHour = currHour

    return streaming, streamHour, wasStreaming

        
async def moveNewTime(currHour, lastHour, guild):
    if currHour != lastHour:
        # Write code here to move people
        print("It is now", hourDic[currHour])
        voiceChannel = await getHourChannel(lastHour, guild)
        destination = await getHourChannel(currHour, guild)

        for member in voiceChannel.members:
            await member.move_to(destination)

    # Will update lastHour if currHour has changed
    lastHour = currHour
    return currHour, lastHour


async def moveInCategory(currHour, guild):
    # Category move
    timeCategory = discord.utils.get(guild.categories, name="Times")
    vcs = timeCategory.voice_channels

    for channel in vcs:
        for member in channel.members:
            if channel.name != hourDic[currHour]:
                destination = await getHourChannel(currHour, guild)
                await member.move_to(destination)


async def getHourChannel(hour, guild):
    return discord.utils.get(guild.voice_channels, name=hourDic[hour])
                    

async def showGamesPlayed(guild):
    # Make dictionary, key = game, list of players = playing
    gameDic = {}
    outText = ""
    guildMembers = guild.members

    for member in guildMembers:
        activity = member.activity
        
        

        #print(member.name + ": " + str(activity))

        if activity != None and (activity.type == discord.ActivityType.playing):         
            aName = activity.name
            #print("Activity Type: " + str(activity.type))
            #print(discord.Activity)

            if aName in gameDic:
                memArray = gameDic.pop(aName)
                memArray.append(member)
                gameDic[aName] = memArray
            else:
                gameDic[aName] = [member]

    if gameDic == {}:
        return "No one is playing anything :("

    for gameKey, players in gameDic.items():
        outText += "__" + str(gameKey) + "__ (" + str(len(players)) + ")\n"

        for player in players:    
            pActivity = player.activity
            state, details = "", ""

            outText += "**" + player.display_name + "**"

            try:
                state, details = pActivity.state, pActivity.details

                if state == None and details == None:
                    outText = outText
                else:
                    outText += " | " + state + " - " + details
                    
            except:
                outText = outText
            
            outText += "\n"

        outText += "\n"

    return outText

