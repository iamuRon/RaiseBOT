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





def setup(bot):
    bot.add_cog(Admin(bot))