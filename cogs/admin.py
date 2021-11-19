from discord.ext import commands
import discord
import random

#-------------------------------------------------------

#              This cog holds admin commands
#              Like kicking and bans

#-------------------------------------------------------


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global channel
        channel = bot.get_channel(818556449030537236)
    
    async def streamTrue(boolean):
        if boolean == True:
            await channel.send(f"LIVE")
        else:
            live = False
            await channel.send(f"NOT LIVE")



def setup(bot):
    bot.add_cog(Admin(bot))