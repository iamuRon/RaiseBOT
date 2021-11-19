from discord.ext import commands
import discord
import random
import sqlite3

db = sqlite3.connect('users.db')
c = db.cursor()

def Sort(li):
    li.sort(key = lambda x: x[1])
    return li

def cleanup(ctx):
    clnList = []
    for i in range(11):
        phs = f"{i}. {ctx[i][0]} has {ctx[i][1]} CaveCoins! \n"
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
        t10List = list(c.execute("SELECT * FROM users WHERE bal>0", ()))
        t10Sorted = Sort(t10List)
        t10Sorted.reverse()
        newt10Sorted = cleanup(t10Sorted)
        newt10 = '\n'.join(str(e) for e in newt10Sorted)
        embed=discord.Embed(title="Top 10 Leaderboard:", description=f"{newt10}", color=0xff00ff)
        embed.set_thumbnail(url="https://i.imgur.com/3QwRkoS.png")
        embed.set_footer(text="Coded by: iamu")
        await ctx.send(embed=embed)

    @commands.command(aliases=['cavecoinsearch'])
    async def ccs(self, ctx, *, user):
        """Search for a users balance"""
        t10List = list(c.execute("SELECT * FROM users WHERE bal>0", ()))
        for i in range(len(t10List)):
            userName = str(t10List[i][0])
            if user in userName:
                embed=discord.Embed(title=f"--- {t10List[i][0]}'s Wallet ---", description=f"Total Cave Coin:", color=0xff00ff)
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
        t10List = Sort(list(c.execute("SELECT * FROM users WHERE bal>0", ())))
        t10List.reverse()
        t10List.pop(0)
        for i in t10List:
            if user in str(i[0]).lower():
                embed=discord.Embed(title="Leaderboard Search:", description=f"{i[0]}'s Total Cave Coin:", color=0xff00ff)
                embed.set_thumbnail(url="https://i.imgur.com/3QwRkoS.png")
                embed.add_field(name=f">> {i[1]} <<", value=f"{i[0]}'s Rank:", inline=False)
                embed.add_field(name=f"{t10List.index(i)+1}", value="___", inline=False)
                embed.set_footer(text="Coded by: Pali")
                await ctx.send(embed=embed)
                return
        await ctx.send(f"Sorry {ctx.author.mention} I couldn't find 'em.")


    # @commands.command(aliases=['leaderboardsearch','pali'])
    # async def lbs(self, ctx, *, user):
    #     """Search for a user's leaderboard rank"""
    #     t10List = Sort(list(c.execute("SELECT * FROM users WHERE bal>0", ())))
    #     t10List.reverse()
    #     t10List.pop(0)
    #     for i in t10List:
    #         if user in str(i[0]).lower():
    #             embed=discord.Embed(title="Leaderboard Search:", color=0xff00ff)
    #             embed.set_thumbnail(url="https://i.imgur.com/3QwRkoS.png")
    #             embed.add_field(name=f"{i[0]} has a total of {i[1]} Cave Coin!", value=f"{i[0]}'s Rank: {t10List.index(i)+1}", inline=False)
    #             embed.set_footer(text="Coded by: Pali")
    #             await ctx.send(embed=embed)
    #             return
    #     await ctx.send(f"Sorry {ctx.author.mention} I couldn't find 'em.")


                
        


def setup(bot):
    bot.add_cog(LB(bot))