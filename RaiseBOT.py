'''
RaiseBOT by iamu & PaliKai
11/3/2021
Version: 0.0.0.0.0.1

https://github.com/Pycord-Development/pycord
https://docs.pycord.dev/en/master/index.html
https://docs.pycord.dev/en/master/api.html

'''
import config
from discord import message
from discord.ext import commands, tasks
import discord
import json
import os
import sqlite3
from itertools import cycle
import asyncio
 
intents = discord.Intents.all()

bot = commands.Bot(command_prefix= ".", intents = intents)

db = sqlite3.connect('users.db')
c = db.cursor()

active_databases = ['users']

def db_add(user):
    name = str(user)
    c.execute("INSERT INTO users VALUES (?, ?)", (name, 0))
    db.commit()

def db_balInc(user):
    userName = str(user)
    userInfo = db_lookup(userName)
    userBal = int(userInfo[0][1])
    newUserBal = userBal + 1
    c.execute("UPDATE users SET bal=? WHERE user=?", (newUserBal, userName))
    db.commit()

def db_update(ctx):
    pass

def db_remove(ctx):
    pass

def db_lookup(user):
    userStr = str(user)
    findUser = list(c.execute("SELECT * FROM users WHERE user=?", (userStr,)))
    if len(findUser) == 0:
        db_add(user)
        userStr = str(user)
        findUser = c.execute("SELECT * FROM users WHERE user=?", (userStr,))
        db.commit()
        return findUser
    else:
        db.commit()
        return findUser

class MyClient(discord.Client):
    


    @bot.event
    async def on_ready():
        ping = int(bot.latency * 1000)
        print(f"Logged in as: {bot.user} | {ping}ms\n" + f"Active Database(s): {active_databases}\n" + "--------")
        serverCount = len(list(bot.guilds))
        status = ['Use .help for commands','Coded by: iamu & PaliKai', f'A part of {serverCount} servers!']
        displaying = cycle(status)
        running = True
        while running:
            currentStatus = next(displaying)
            await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=currentStatus ,type=2))
            await asyncio.sleep(20)

    @bot.event
    async def on_join(member):
        db_add(member.user)
         


    @bot.event
    async def on_message(message):
        context = [f"Server: {message.author.guild} -> Channel: {message.channel} -> User: {message.author} | {message.created_at} : {message.content}"]
        with open("chatlog.txt", "a") as chatlog:
            chatlog.write(f"{context}\n")
        chatlog.close()
        db_lookup(message.author)
        db_balInc(message.author)
        await bot.process_commands(message)



@bot.command()
async def ping(ctx):
        """Pong!"""
        ping = int(bot.latency * 1000)
        await ctx.send(f"Pong! | {ping}ms")

@bot.command(aliases=['balance', 'wallet', 'cc', 'CaveCoin', 'cavecoin'])
async def bal(ctx):
    """Displays your balance in the CaveCoin wallet!"""
    balance = db_lookup(ctx.author)
    strBal = balance[0][1]
    userBal = strBal
    embed=discord.Embed(title="Balance", color=0xff00f7)
    embed.set_author(name="RaiseBot")
    embed.add_field(name=f"--- {ctx.author}'s Wallet ---", value=f"Your CaveCoin: {userBal}", inline=False)
    embed.set_footer(text="Coded by: iamu")
    await ctx.send(f"Here you go {ctx.author.mention} !")
    await ctx.send(embed=embed)
            



        
            
            
            








'''



Dont Touch Below This Comment as it is starting parameters



'''

client = MyClient()

initial_extensions = ["cogs.commands", "cogs.palisprojects", "cogs.media"]

print("Running Setup...")

for extension in initial_extensions:
    bot.load_extension(extension)
    print(f"Loaded '{extension}'...")

print("Setup Complete...")

bot.run(config.TOKEN)



























'''FOUR LINES'''