'''
RaiseBOT by iamu & PaliKai
11/3/2021
Version: 0.0.0.0.0.1

https://github.com/Pycord-Development/pycord
https://docs.pycord.dev/en/master/index.html
https://docs.pycord.dev/en/master/api.html

'''
import config
from discord import channel, message
from discord.ext import commands, tasks
import discord
import json
import os
import sqlite3
from itertools import cycle
import asyncio
import json
import requests
from discord.ext import tasks
from twitchAPI.twitch import Twitch

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

#-------------------------------------------------------

#              This holds twitch live notifications I *USED TO NOT* KNOW WAT THE FUCK THIS EVEN DOES I WILL LOOK INTO LATER JUST WANNA KNOW IF IT WORKS

#-------------------------------------------------------

@tasks.loop(seconds=10)
async def twitchstream():
    with open('streamers.txt', 'r') as file:
        streamers = list(file.readlines())
    for i in streamers:
        if "\n" in i:
            StName = i.strip()
            with open('channelids.txt', 'r') as file:
                channels = list(file.readlines())
            for i in channels:
                if "\n" in i:
                    channelid = i.strip()
                    newIDint = int(channelid)
            await streamer(StName, newIDint)


async def streamer(name, channelid):
    StName = name
    placeholderList = []
    channel = bot.get_channel(channelid)
    client_id = 'iew89f33r9gr771zwbmhen4d2guu7i'
    client_secret = 'oghcuhwz9c3pzrwe1r8itp3x9qe44g'
    body = {'client_id': client_id,'client_secret': client_secret,"grant_type": 'client_credentials'}
    r = requests.post('https://id.twitch.tv/oauth2/token', body)
    keys = r.json()
    headers = {'Client-ID': client_id,'Authorization': 'Bearer ' + keys['access_token']}
    stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + StName, headers=headers)
    stream_data = stream.json()
    if len(stream_data['data']) == 1:
        placeholderList.append(StName)
        placeholder = StName + ' is live: ' + stream_data['data'][0]['title'] + ' playing ' + stream_data['data'][0]['game_name']
        async for history in channel.history(limit=200):
            if StName not in history.content:
                for i in placeholderList:
                    if i != StName:
                        await channel.send(placeholder)
                        return
                else:
                    return
    else:
        if StName in placeholderList:
            placeholderList.remove(StName)
            print(placeholderList)
        else:
            return
    



#-------------------------------------------------------

#              This holds twitch live notifications I *USED TO NOT* KNOW WAT THE FUCK THIS EVEN DOES I WILL LOOK INTO LATER JUST WANNA KNOW IF IT WORKS

#-------------------------------------------------------


class MyClient(discord.Client):
    


    @bot.event
    async def on_ready():
        ping = int(bot.latency * 1000)
        print(f"Logged in as: {bot.user} | {ping}ms\n" + f"Active Database(s): {active_databases}\n" + "--------")
        serverCount = len(list(bot.guilds))
        status = ['Use .help for commands','Coded by: iamu & PaliKai', f'A part of {serverCount} servers!']
        displaying = cycle(status)
        running = True
        await twitchstream.start()
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
        try:
            with open("chatlog.txt", "a") as chatlog:
                chatlog.write(f"{context}\n")
            chatlog.close()
        except UnicodeError:
            pass
        db_lookup(message.author)
        db_balInc(message.author)
        try:
            if message.content[0] != '.':
             return
            else:
                await bot.process_commands(message)
        except IndexError:
            return


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
    embed.set_thumbnail(url="https://i.imgur.com/3QwRkoS.png")
    embed.add_field(name=f"--- {ctx.author}'s Wallet ---", value=f"Your CaveCoin: {userBal}", inline=False)
    embed.set_footer(text="Coded by: iamu")
    await ctx.send(f"Here you go {ctx.author.mention} !")
    await ctx.send(embed=embed)
            
@bot.command(name='addtwitch', help='Adds your Twitch to the live notifs. (ADMIN ONLY)', pass_context=True)
async def add_twitch(ctx, twitch_name):
    if ctx.author.guild_permissions.administrator:
        # Adds the changes we made to the json file.
        with open('streamers.txt', 'a') as file:
            file.writelines(f"{twitch_name}\n")
        # Tells the user it worked.
        await ctx.send(f"Added {twitch_name} for {ctx.author} to the notifications list.")
    else:
        await ctx.send(f"Sorry bozo you're not the boss of me!")

@bot.command(name='twitchchannel', aliases=['streamnotif'])
async def add_twitch_notification_channel(ctx, channelID):
    """Declares a channel in the server to be the twitch notif channel (ADMIN ONLY)"""
    if ctx.author.guild_permissions.administrator:
        with open('channelids.txt', 'a') as file:
            file.writelines(f"{channelID}\n")
        # Tells the user it worked.
        await ctx.send(f"Added {channelID} for {ctx.author} to the notifications list.")
    else:
        await ctx.send(f"Sorry bozo you're not the boss of me!")
            
            
            








'''



Dont Touch Below This Comment as it is starting parameters



'''

client = MyClient()

initial_extensions = ["cogs.commands", "cogs.palisprojects", "cogs.media", "cogs.leaderboard"]

print("Running Setup...")

for extension in initial_extensions:
    bot.load_extension(extension)
    print(f"Loaded '{extension}'...")

print("Setup Complete...")

bot.run(config.TOKEN)



























'''FOUR LINES'''