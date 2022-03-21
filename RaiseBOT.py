'''
RaiseBOT by iamu & PaliKai
11/3/2021
Version: 0.0.0.0.0.1

https://github.com/Pycord-Development/pycord
https://docs.pycord.dev/en/master/index.html
https://docs.pycord.dev/en/master/api.html

'''
from ast import alias
import os
from asyncio.windows_events import NULL
from discord import channel
import config
from discord.ext import commands, tasks
import discord
import json
import sqlite3
from asyncio import sleep
import json
import requests
from discord.ext import tasks
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.2/bin")
import tensorflow as tf
import aiohttp
import shutil
from keras.models import sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras import layers
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import cifar10
plt.style.use('fivethirtyeight')

(x_train, y_train), (x_test, y_test) = cifar10.load_data()

intents = discord.Intents.all()

bot = commands.Bot(command_prefix= ".", intents = intents)

#=============================
#  DATABASE / SQL
#=============================

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

#              This holds twitch live notifications

#-------------------------------------------------------
global twitchLiveList
twitchLiveList = []
newStreamerList = []
@tasks.loop(seconds=60)
async def streamer():
    with open('streamers.json', 'r') as file:
        streamers = list(json.loads(file.read()))
        for i in streamers:
            StName = i[22:]
            channelURL = i
            with open('channelids.txt', 'r') as file:
                    channels = list(file.readlines())
            print("Opening channel id's")
            client_id = config.ID
            client_secret = config.SECRET
            body = {'client_id': client_id,'client_secret': client_secret,"grant_type": 'client_credentials'}
            r = requests.post('https://id.twitch.tv/oauth2/token', body)
            keys = r.json()
            try:
                headers = {'Client-ID': client_id,'Authorization': 'Bearer ' + keys['access_token']}
                stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + StName, headers=headers)
                stream_data = stream.json()
                print(f"trying to get data... from {StName}")
                try:
                    print("attempting")
                    if len(stream_data['data']) == 1:
                        print(f"verifying data... for {StName}")
                        if StName not in twitchLiveList:
                            with open('whitelist.json', 'r') as file:
                                whitelistList = json.loads(file.read())
                                
                            for key in whitelistList:
                                print(f"Checking if {StName} is in Whitelist...")
                                value = whitelistList[key]
                                # print(value)
                                if StName in value[1]:
                                    # print('value')
                                    embed=discord.Embed(title=f":red_circle: --- {StName.upper()} IS LIVE --- :red_circle:", description=f"{stream_data['data'][0]['title']}", color=0xff00ff)
                                    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Twitch_Glitch_Logo_Purple.svg/878px-Twitch_Glitch_Logo_Purple.svg.png")
                                    embed.add_field(name=f">>  __PLAYING__  <<", value = f" _'{stream_data['data'][0]['game_name']}'_", inline=False)
                                    embed.set_footer(text="Coded by: iamu")
                                    for i in channels:
                                        print(f"Checking {i}")
                                        wlChannel = int(value[0])
                                        newChannel = int(i)
                                        if newChannel == wlChannel:
                                            
                                            for x in value[1]:
                                                print(f"Verifying that {StName} is in whitelist...")
                                                
                                                if StName == x:
                                                    channelid = i
                                                    
                                                    newIDint = int(channelid)
                                                    channel = bot.get_channel(newIDint)
                                                    # allowed_mentions = discord.AllowedMentions(everyone = True)
                                                    # await channel.send(content = "@everyone", allowed_mentions = allowed_mentions)
                                                    await channel.send(embed=embed)
                                                    await channel.send(f">>> {channelURL}")
                                                    print(f"Posted {StName} is Live!")
                                                    if StName not in twitchLiveList:
                                                        print(f"Added {StName} to 'Live Users'")
                                                        twitchLiveList.append(StName)
                                                    else:
                                                        continue
                                                else:
                                                    continue
                                        else:
                                            print(f"{StName} is NOT whitelisted for {i}")
                                            continue
                                else:
                                    continue
                        else:
                            print(f'Current Live users: {twitchLiveList}')
                            continue
                    else:
                        print("no data found, checking if they went offline...")
                        if StName in twitchLiveList:
                            print(f"Removing {StName} from 'Live Users'")
                            with open('whitelist.json', 'r') as file:
                                whitelistList = json.loads(file.read())
                            with open('channelids.txt', 'r') as file:
                                channels = list(file.readlines())
                            for key in whitelistList:
                                value = whitelistList[key]
                                print(value)
                                if StName in value[1]:
                                    embed=discord.Embed(title=f":black_circle: --- {StName.upper()}'s Stream has ended!' --- :black_circle:", description=f"----------", color=0xff00ff)
                                    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Twitch_Glitch_Logo_Purple.svg/878px-Twitch_Glitch_Logo_Purple.svg.png")
                                    embed.add_field(name=f">>  Check below to watch what you missed!  <<", value = "-", inline=False)
                                    embed.set_footer(text="Coded by: iamu")
                                    for i in channels:
                                        wlChannel = int(value[0])
                                        newChannel = int(i)
                                        if newChannel == wlChannel:
                                            for x in value[1]:
                                                if StName == x:
                                                    channelid = i
                                                    newIDint = int(channelid)
                                                    newIDint = int(channelid)
                                                    channel = bot.get_channel(newIDint)
                                                    await channel.send(embed=embed)
                                                    await channel.send(f">>> {channelURL}")
                                                    print(f"Posted {StName} is offline...")
                                                    if StName in twitchLiveList:
                                                        print(f"Removed {StName} from 'Live Users'")
                                                        twitchLiveList.remove(StName)
                                                    else:
                                                        continue
                        else:
                            print("No data and streamer hasnt gone live yet")
                            continue
                except KeyError:
                    print("Something went Horribly Wrong...  KEYERROR")
                    continue
            except KeyError:
                print("Something went horribly wrong... KEYERROR")
                continue


#-------------------------------------------------------

#              This holds twitch live notifications

#-------------------------------------------------------

async def status():
        streamer.start()
        serverCount = len(list(bot.guilds))
        status = ['Use .help for commands','Coded by: iamu & PaliKai', f'A part of {serverCount} servers!']
        while True:
            for i in status:
                await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=i ,type=2))
                await sleep(10)

#=============================
#  REACTION ROLES START HERE
#=============================
with open("reactionServers.json") as jsonFile:
    guildReactions = json.load(jsonFile)
    print(guildReactions)

#=============================
#  REACTION ROLES PAUSE HERE
#=============================


#=============================
#           MAIN
#=============================
class MyClient(discord.Client):
    


    @bot.event
    async def on_ready():
        ping = int(bot.latency * 1000)
        print(f"Logged in as: {bot.user} | {ping}ms\n" + f"Active Database(s): {active_databases}\n" + "--------")
        await bot.loop.create_task(status())
        

    @bot.event
    async def on_join(member):
        db_add(member.user)
         


    @bot.event
    async def on_message(message):
        try:
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
        except AttributeError:
            return

#=============================
#  Default Commands
#=============================

@bot.command()
async def ping(ctx):
        """Pong!"""
        ping = int(bot.latency * 1000)
        await ctx.send(f"Pong! | {ping}ms")

#=============================
#  Currency Lookup
#=============================

@bot.command(aliases=['balance', 'wallet', 'cc', 'CaveCoin', 'cavecoin'])
async def bal(ctx):
    """Displays your balance in the CaveCoin wallet!"""
    with open('currency.json', 'r') as file:
        currencyChange = json.loads(file.read())
    userCheck = currencyChange
    guildCheck = str(ctx.author.guild)
    if guildCheck not in userCheck:
        await ctx.send(f'Sorry {ctx.author.mention}, this server has not defined a currency yet!')
        return
    else:
        balance = db_lookup(ctx.author)
        strBal = balance[0][1]
        userBal = strBal
        embed=discord.Embed(title="Balance", color=0xff00f7)
        embed.set_author(name="RaiseBot")
        embed.set_thumbnail(url="https://i.imgur.com/3QwRkoS.png")
        embed.add_field(name=f"--- {ctx.author}'s Wallet ---", value=f"Your {userCheck[guildCheck][1]}: {userBal}", inline=False)
        embed.set_footer(text="Coded by: iamu")
        await ctx.send(f"Here you go {ctx.author.mention} !")
        await ctx.send(embed=embed)

#===========================================
#  Twitch Live Notification Setup Commands
#===========================================
@bot.command(name='addtwitch', help='Adds your Twitch to the live notifs. (ADMIN ONLY)', pass_context=True)
async def add_twitch(ctx, *, twitch_name):
    if ctx.author.guild_permissions.administrator:
        twitch_name = twitch_name.split()
        if (len(twitch_name) != 2):
            await ctx.send("Syntax: .addtwitch <twitch channel name> <twitch URL>")
            return
        with open('streamers.json', 'r') as file:
            streamers = json.loads(file.read())
        streamers[twitch_name[1]] = twitch_name[0]
        with open('streamers.json', 'w') as file:
            file.write(json.dumps(streamers))
        await ctx.send(f"Added {streamers} for {ctx.author.mention} to the notifications list.")
    else:
        await ctx.send(f"Sorry bozo you're not the boss of me!")

@bot.command(name='twitchchannel', aliases=['streamnotif'])
async def add_twitch_notification_channel(ctx, channelID):
    """Declares a channel in the server to be the twitch notif channel (ADMIN ONLY)"""
    if ctx.author.guild_permissions.administrator:
        with open('channelids.txt', 'a') as file:
            file.writelines(f"{channelID}\n")
        await ctx.send(f"Added {channelID} for {ctx.author.mention} to the channel list.")
    else:
        await ctx.send(f"Sorry bozo you're not the boss of me!")

@bot.command(name='wl', help='Makes a whitelist to block unwanted streamers from notifs (ADMIN ONLY)', pass_context=True)
async def whitelist(ctx, *, streamers):
    if ctx.author.guild_permissions.administrator:
        if ' ' in streamers:
            newStreamers = streamers.split()
            with open('whitelist.json', 'r') as file:
                wlStreamers = json.loads(file.read())
            print(wlStreamers)
            server = str(ctx.author.guild)
            channelid = int(ctx.channel.id)
            cInfo = [server, channelid]
            for i in newStreamers:
                cInfo.append(i)
            wlStreamers[cInfo[0]] = [cInfo[1], cInfo[2:]]
            with open('whitelist.json', 'w') as file:
                file.write(json.dumps(wlStreamers))
            await ctx.send(f"Added {wlStreamers} for {ctx.author.mention} to the notifications list.")
        else:
            with open('whitelist.json', 'r') as file:
                wlStreamers = json.loads(file.read())
            print(wlStreamers)
            server = str(ctx.author.guild)
            channelid = int(ctx.channel.id)
            cInfo = [server, channelid]
            streamersList = [streamers]
            wlStreamers[cInfo[0]] = [cInfo[1], streamersList]
            with open('whitelist.json', 'w') as file:
                file.write(json.dumps(wlStreamers))
            await ctx.send(f"Added {wlStreamers} for {ctx.author.mention} to the notifications list.")
    else:
        await ctx.send(f"Sorry bozo you're not the boss of me!")

#=============================
#  REACTION ROLES RESUME HERE
#=============================
@bot.event
async def on_raw_reaction_add(payload):
    if bot.get_user(payload.user_id) != bot.user:
        rr = (payload.guild_id,payload.channel_id,payload.message_id,None)
        for x in guildReactions:
            if (isSameMessageAs(rr,x)):
                for y in x[3]:
                    if (str(y[0]) == str(payload.emoji)):
                        guild = bot.get_guild(payload.guild_id)
                        member = guild.get_member(payload.user_id)
                        await member.add_roles(guild.get_role(y[1]))

@bot.event
async def on_raw_reaction_remove(payload):
    if bot.get_user(payload.user_id) != bot.user:
        rr = (payload.guild_id,payload.channel_id,payload.message_id,None)
        for x in guildReactions:
            if (isSameMessageAs(rr,x)):
                for y in x[3]:
                    if (str(y[0]) == str(payload.emoji)):
                        guild = bot.get_guild(payload.guild_id)
                        member = guild.get_member(payload.user_id)
                        await member.remove_roles(guild.get_role(y[1]))

@bot.event
async def on_raw_message_delete(payload):
    rr = (payload.guild_id,payload.channel_id,payload.message_id,None)
    for x in guildReactions:
        if (isSameMessageAs(rr,x)):
            guildReactions.remove(x)
    updateJSON()

def createReactionRole(guild,channel,message,reaction,role):
    rr = (guild,channel,message,[(reaction,role)])
    for x in guildReactions:
        if (isSameMessageAs(x,rr)):
            if not (x[3] in ((reaction,role))):
                x[3].append((reaction,role))
                return
    guildReactions.append(rr)


@bot.command()
# .reactionRole "Embed Title" "Embed Description" (🐶 954468370156236840) (💀 954500389795942460)
async def reactionRole(ctx, *args):
    try:
        if(ctx.author.guild_permissions.administrator):
            embed=discord.Embed(title=args[0], description=args[1])
            message = await ctx.send(embed=embed)
            reactionroles = []
            for i in range(int((len(args)-2)/2)):
                str1 = str(str(args[i*2+2]) + " " + str(args[i*2+3]))
                str1 = str1.replace("(","").replace(")","")
                reactionroles.append(str1)
                for x in reactionroles:
                    tup = tuple(map(str, x.split(' ')))
                    await message.add_reaction(tup[0])
                    roleID = str(tup[1].replace("<@&","").replace(">",""))
                    createReactionRole(ctx.guild.id,ctx.channel.id,message.id,str(tup[0]),int(roleID))
            updateJSON()
        else:
            await ctx.send("You need to be an administrator to use this command!")
    except ValueError:
            await ctx.send('ERROR: PLEASE USE THIS SYNTAX!!!(WiP) \n.reactionRole "Embed Title" "1️⃣ : Role1\n2️⃣ : Role2" (1️⃣ @Role1) (2️⃣ @Role2)')

@reactionRole.error
async def play_error(ctx, error):
    if isinstance(error, discord.errors.HTTPException):
        await ctx.send('Error: PLEASE USE THIS SYNTAX!!!(WiP)\nSyntax: .reactionRole "Embed Title" "1️⃣ : Role1\n2️⃣ : Role2" (1️⃣ @Role1) (2️⃣ @Role2)')
        return


@bot.command()
async def embed(ctx, title, description):
    embed=discord.Embed(title=title, description=description)
    await ctx.send(embed=embed)

@bot.command()
async def me(ctx):
    msg = "Hi " + ctx.author.mention
    await ctx.send(msg)

def updateJSON():
    with open('reactionServers.json', 'w') as jsonFile:
        json.dump(guildReactions, jsonFile)
        jsonFile.close()

    
def isSameMessageAs(tup1,tup2):
    if (tup1[0] == tup2[0]):
        if (tup1[1] == tup2[1]):
            if (tup1[2] == tup2[2]):
                return True
    return False
            
            
#=============================
#  REACTION ROLES END HERE
#=============================

#=============================
#  Image Recognition
#=============================
@bot.command(alias = ['ir'])
async def imagerecognition(ctx, url):
    '''Image Recognition! .ir [url]'''
    print("IT WORKED")
    image_url = url
    img_data = requests.get(image_url).content
    with open('recognitionImages/image_name.jpg', 'wb') as handler:
        handler.write(img_data)






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