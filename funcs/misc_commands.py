import discord

async def printBruh(argument):
    if len(argument) == 0:
        return "bruh momento"  

    try:
        amount = int(argument)
        
        if amount > 400 or amount < -400:
            return "it's too long, bruh"
        elif amount == 0:
            return "no bruh"
        elif amount < 0:
            return "hurb " * -amount
        else:
            return "bruh " * amount
    except:
        return "enter a NUMBER bruh"
