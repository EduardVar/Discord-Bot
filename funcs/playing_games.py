import datetime
import pytz
import discord

specialGames = ["League of Legends", "Call of Duty®: Modern Warfare®"]

async def showGamesPlayed(guild):
    # Make dictionary, key = game, list of players = playing
    gameDic = {}
    guildMembers = guild.members

    for member in guildMembers:
        activity = member.activity

        if activity != None and (activity.type == discord.ActivityType.playing):         
            aName = activity.name

            if aName in gameDic:
                memArray = gameDic.pop(aName)
                memArray.append(member)
                gameDic[aName] = memArray
            else:
                gameDic[aName] = [member]

    # Will have to split up code here between two functions

    if gameDic == {}:
        return "No one is playing anything :("

    oldZone = pytz.timezone('UTC')
    newZone = pytz.timezone("US/Eastern")

    outText = ""

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
                    outText += " | " + details + " - " + state + " "
            except:
                outText = outText

            # pActivity.start returns date time! Find elapsed time
            if pActivity.start != None:
                localizedTime = oldZone.localize(pActivity.start)
                adjustedTime = localizedTime.astimezone(newZone)
                naiveStart = adjustedTime.replace(tzinfo=None)
                
                diff = datetime.datetime.now() - naiveStart
                diff = (int)(diff.total_seconds()) # Converts to seconds
                
                secsInMin = 60
                secsInHour = secsInMin * 60
                           
                hours = divmod(diff, secsInHour)[0]
                mins = divmod(diff, secsInMin)[0]
                secs = diff % 60

                if gameKey not in specialGames:
                    if hours == 0 and mins <= 1:
                        outText += "`Just started playing`"
                    elif hours == 0:
                        outText += "`for " + str(mins) + " minute"

                        if mins > 1:
                            outText += "s`"
                        else:
                            outText += "`"
                    else:
                        outText += "`for " + str(hours) + " hour"

                        if hours > 1:
                            outText += "s`"
                        else:
                            outText += "`"
                else:
                    outText += "`"
                    
                    if hours >= 1:
                        outText += str(hours).zfill(2)
                        
                    outText += str(mins).zfill(2) + ":" + str(secs).zfill(2)
                    outText += " elapsed`"
            
            outText += "\n"

        outText += "\n"

    return outText
