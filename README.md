# Discord-Bot
Python-based virtual bot to manage and automatize personal discord server.

## Features
* The server has a voice channel for each hour of the day (from 12 am to 11 pm). These voice channels are all sorted under the TIME category. Will automatically move users to the correct voice channel depending on what time of the day it is. 
  * (Ex: at 4:32 pm, all users that are in voice communications for the server will reside in the *4 pm* voice channel. At 5:00 pm, all users in the *4 pm* voice channel are moved by the bot to the *5 pm* voice channel)
  * Any user who joins the wrong voice channel will be automatically moved to the correct voice channel. (Updates every second)
  * Additional functionality regarding if a user is streaming through discord in one of the timed voice channels. Every time a user moves from one voice channel to another, their stream ends and the streamer has to restart it.
    * On bot launch, checks if anyone is streaming in any of the voice channels. Make's sure to wait for all streams to end before moving users to the correct channel.
    * In addition, if a user is already streaming upon a time change, will send each streaming user a message and mention them in the general chat.
      * Once, all users are not streaming, will automatically move all members in voice chat to the correct channel.
    * Checks if user in the correct channel ever 1 second (since start of the bot).

## Commands
Type **~help** for info on what commands are available

### Using the "~" prefix
| Command | Description |
| --- | --- |
| admin | Sends an image of the admin consequences |
| assemble | @ the AvengerBots |
| aww | Sends an image from r/awwnime |
| blursed | Sends an image from r/blusedimages |
| bruh | You can add a number after bruh to repeat the phrase [-400, 400] |
| cursed | Sends an image from r/cursedimages |
| games? | Shows what games people are playing |
