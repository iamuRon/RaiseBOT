from discord.ext import commands
import discord
import random

from discord.ext.commands import bot

from RaiseBOT import db_lookup, db_add
import sqlite3

db = sqlite3.connect('users.db')
c = db.cursor()

class Pali(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['rockpaperscissors'])
    async def rps(self, ctx, *, txt):
        """Play Rock, Paper, Scissors! AND WAGER YOUR MONAYYYYY"""
        validTypes = ["rock","paper","scissors"]
        txt = txt.split()
        if (len(txt) != 2):
            await ctx.send("Cyntax: .rps <answer> <wager>")
            return
        if (int(db_lookup(str(ctx.author))[0][1]) < int(txt[1])):
            await ctx.send("You cannot wager more than you have!")
            return
        response = random.choices(validTypes,k=1)[0]
        if (txt[0] in validTypes):
            if (response == txt[0]):
                await ctx.send("Draw!")
                return
            else:
                result = False
                if (txt[0] == "rock"):
                    if (response == "paper"):
                        result = True
                    else:
                        result = False
                elif (txt[0] == "paper"):
                    if (response == "scissors"):
                        result = True
                    else:
                        result = False
                elif (txt[0] == "scissors"):
                    if (response == "rock"):
                        result = True
                    else:
                        result = False
            userName = str(ctx.author)
            userInfo = db_lookup(userName)
            userBal = int(userInfo[0][1])
            if (result):
                result = "I win!"
                userBal-=int(txt[1])
            else:
                result = "You win!"
                userBal+=int(txt[1])
            embed=discord.Embed(title=result, color=0xff00ff)
            embed.set_author(name="Rock Paper Scissors")
            embed.add_field(name="New Balance: ", value=f"{userBal}", inline=True)
            embed.set_footer(text="Coded by: Pali : )")
            await ctx.send(f"I chose {response}!")
            await ctx.send(embed=embed)
            c.execute("UPDATE users SET bal=? WHERE user=?", (userBal, userName))
            db.commit()
    
    @commands.command(aliases=['coinflip','flip'])
    async def coin(self, ctx):
        """Flips a coin, returning either Heads or Tails!"""
        if (random.randint(0,2) == 0):
            embed=discord.Embed(title="Heads!", color=0xff00ff)
            #embed.set_image(url="https://www.nicepng.com/png/full/395-3951330_thecoinspot-com-us-washington-head-quarter-dollar-coin.png")
            embed.set_thumbnail(url="https://www.nicepng.com/png/full/395-3951330_thecoinspot-com-us-washington-head-quarter-dollar-coin.png")
            embed.set_author(name="Coinflip")
            embed.set_footer(text="Coded by: Pali")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="Tails!", color=0xff00ff)
            #embed.set_image(url="https://www.nicepng.com/png/full/146-1464848_quarter-tail-png-tails-on-a-coin.png")
            embed.set_thumbnail(url="https://www.nicepng.com/png/full/146-1464848_quarter-tail-png-tails-on-a-coin.png")
            embed.set_author(name="Coinflip")
            embed.set_footer(text="Coded by: Pali")
            await ctx.send(embed=embed)
        
    @commands.command(aliases=['gmame'])
    async def game(self, ctx):
        i = 0
        txt=["@","#","#","#","#","#","#","#","#","#"]
        message = await ctx.send("".join(txt))
        while(i<10):
            i+=1
            await message.edit(content="".join(txt))
            txt.insert(0, txt.pop(-1))
        await message.edit(content="##########")
        print("done")

    @rps.error
    async def rps_error(self, ctx, error):
        if isinstance(error, ValueError):
            await ctx.send('Error: Syntax: .rps [choice] [amount]')
            return 

#------------------------------------------------------
#   Hello Pali this file is for you. you can put your 
#   code in below. You can also refer to the other functions
#   from the other cog or also from the main bot folder.
#   note: if you want to use a listener it will have to be implemented
#   in a different way than from RaiseBOT.py
#   Go crazy and upload either all files or just upload this one
#   whichever you find to be easier.
#------------------------------------------------------


def setup(bot):
    bot.add_cog(Pali(bot))