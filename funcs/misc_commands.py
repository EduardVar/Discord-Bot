import discord

async def printBruh(argument):
    if len(argument) == 0:
        return "bruh momento"  

    try:
        amount = int(argument)
        
        if amount > 400:
            return "it's too long, bruh"
        else:
            return "bruh " * amount
    except:
        return "enter a NUMBER bruh"
