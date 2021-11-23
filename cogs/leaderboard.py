from discord.errors import DiscordException, DiscordServerError
from discord.ext import commands
import discord
import random
import sqlite3
import json

from discord.ext.commands.errors import MissingRequiredArgument

db = sqlite3.connect('users.db')
c = db.cursor()

def Sort(li):
    li.sort(key = lambda x: x[1])
    return li

def cleanup(ctx, author):
    with open('currency.json', 'r') as file:
            currencyChange = json.loads(file.read())
    newUserCheck = currencyChange
    newGuildCheck = author
    clnList = []
    for i in range(11):
        phs = f"{i}. {ctx[i][0]} has {ctx[i][1]} {newUserCheck[newGuildCheck][1]}'s! \n"
        clnList.append(phs)
    clnList.remove(clnList[0])
    return clnList
        

"""
Pyfro's Currency: PyFrog's
get cave coin + pyfrog working independent of one another
"""



class LB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['LB'])
    async def lb(self, ctx):
        """Displays top 10 users"""
        with open('currency.json', 'r') as file:
            currencyChange = json.loads(file.read())
        userCheck = currencyChange
        guildCheck = str(ctx.author.guild)
        if guildCheck not in userCheck:
            await ctx.send(f'Sorry {ctx.author.mention}, this server has not defined a currency yet!')
            return
        else:
            print(userCheck)
            t10List = list(c.execute("SELECT * FROM users WHERE bal>0", ()))
            t10Sorted = Sort(t10List)
            t10Sorted.reverse()
            newt10Sorted = cleanup(t10Sorted, guildCheck)
            newt10 = '\n'.join(str(e) for e in newt10Sorted)
            embed=discord.Embed(title="Top 10 Leaderboard:", description=f"{newt10}", color=0xff00ff)
            embed.set_thumbnail(url="https://i.imgur.com/3QwRkoS.png")
            embed.set_footer(text="Coded by: iamu")
            await ctx.send(embed=embed)

    @commands.command(aliases=['cavecoinsearch'])
    async def ccs(self, ctx, *, user):
        """Search for a users balance"""
        with open('currency.json', 'r') as file:
            currencyChange = json.loads(file.read())
        userCheck = currencyChange
        guildCheck = str(ctx.author.guild)
        if guildCheck not in userCheck:
            await ctx.send(f'Sorry {ctx.author.mention}, this server has not defined a currency yet!')
            return
        else:
            t10List = list(c.execute("SELECT * FROM users WHERE bal>0", ()))
            for i in range(len(t10List)):
                userName = str(t10List[i][0])
                if user in userName:
                    embed=discord.Embed(title=f"--- {t10List[i][0]}'s Wallet ---", description=f"Total {userCheck[guildCheck][1]}'s:", color=0xff00ff)
                    embed.set_thumbnail(url="https://i.imgur.com/3QwRkoS.png")
                    embed.add_field(name=f">>  {t10List[i][1]}  <<", value = "___", inline=False)
                    embed.set_footer(text="Coded by: iamu")
                    await ctx.send(embed=embed)
                    userInUserName = True
                    break
                else:
                    userInUserName = False
                    continue
            if userInUserName != True:
                await ctx.send(f"Sorry {ctx.author.mention} I couldn't find 'em.")




    @commands.command(aliases=['leaderboardsearch','pali'])
    async def lbs(self, ctx, *, user):
        """Search for a user's leaderboard rank"""
        with open('currency.json', 'r') as file:
            currencyChange = json.loads(file.read())
        userCheck = currencyChange
        guildCheck = str(ctx.author.guild)
        if guildCheck not in userCheck:
            await ctx.send(f'Sorry {ctx.author.mention}, this server has not defined a currency yet!')
            return
        else:
            t10List = Sort(list(c.execute("SELECT * FROM users WHERE bal>0", ())))
            t10List.reverse()
            t10List.pop(0)
            for i in t10List:
                if user.lower() in str(i[0]).lower():
                    embed=discord.Embed(title="Leaderboard Search:", description=f"{i[0]}'s Total {userCheck[guildCheck][1]}'s:", color=0xff00ff)
                    embed.set_thumbnail(url="https://i.imgur.com/3QwRkoS.png")
                    embed.add_field(name=f">> {i[1]} <<", value=f"{i[0]}'s Rank:", inline=False)
                    embed.add_field(name=f"{t10List.index(i)+1}", value="___", inline=False)
                    embed.set_footer(text="Coded by: Pali")
                    await ctx.send(embed=embed)
                    return
            await ctx.send(f"Sorry {ctx.author.mention} I couldn't find 'em.")

    
    global currency
    @commands.command(aliases=['chcr'])
    async def changecurrency(self, ctx, *, currency):
        """Changes the name of the currency (ADMIN ONLY)"""
        if ctx.author.guild_permissions.administrator:
            server = str(ctx.author.guild)
            currency = [currency, server]
            with open('currency.json', 'r') as file:
                currencyChange = json.loads(file.read())
            currencyChange[server] = (currency[1], currency[0])
            with open('currency.json', 'w') as file:
                file.write(json.dumps(currencyChange))
            await ctx.send(f"Added {currencyChange} for {ctx.author.mention} to the notifications list.")
        else:
            await ctx.send(f'Sorry {ctx.author.mention}, you are not the boss of me!')

    @changecurrency.error
    async def changecurrency_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Error: Syntax: .chcr <Curreny Name Here>')
            return
                
        


def setup(bot):
    bot.add_cog(LB(bot))