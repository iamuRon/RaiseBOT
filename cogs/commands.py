'''
Discord bot commands
'''
from discord.ext import commands
import discord
import random

from discord.ext.commands import bot

from RaiseBOT import db_add

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
def encrypt(txt, shift):
    str = ""
    for i in range(0,len(txt)):
        str += ((letters[letters.index(txt[i])+shift-len(letters)] if (letters.index(txt[i])+shift > len(letters)-1) else letters[letters.index(txt[i])+shift]) if txt[i] in letters else txt[i]) if ((letters[letters.index(txt[i])+shift-len(letters)] if (letters.index(txt[i])+shift > len(letters)-1) else letters[letters.index(txt[i])+shift]) if txt[i] in letters else txt[i]) == ((letters[letters.index(txt[i])+shift-len(letters)] if (letters.index(txt[i])+shift > len(letters)-1) else letters[letters.index(txt[i])+shift]) if txt[i] in letters else txt[i]).lower() else ((letters[letters.index(txt[i].lower())+shift-len(letters)] if (letters.index(txt[i].lower())+shift > len(letters)-1) else letters[letters.index(txt[i].lower())+shift]) if txt[i].lower() in letters else txt[i].lower()).upper()
    return str

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
        """Ask it a question and get a response!"""
        responses = ['It is certain.', 
                    'It is decidedly so.', 
                    'Without a doubt.',
                    'Yes definitely.',
                    'You may rely on it.',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Signs point to yes.',
                    'Reply hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'Concentrate and ask again.',
                    "Don't count on it.",
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.',
                    'Fuck, I can\'t remember, try again.',
                    'Very doubtful.']
        eBallChoice = random.choices(responses,k=1)[0]
        eBCClean = eBallChoice
        embed=discord.Embed(title="8Ball:", description=f"{eBCClean}", color=0xff00ff)
        embed.set_author(name="RaiseBot")
        embed.add_field(name=f"Your Question: ", value=f"'{question}'", inline=False)
        embed.set_footer(text="Coded by: iamu")
        await ctx.send(f"Here you go {ctx.author.mention} !")
        await ctx.send(embed=embed)

    @commands.command(aliases = ['ed'])
    async def encdec(self, ctx, *, context):
        """Encrypt or Decrypts messages via ROT13 style"""
        ret = encrypt(context,13)
        embed=discord.Embed(title="Encrypted/Decrypted Message:", description=f"{ret}", color=0xff00ff)
        embed.set_author(name="RaiseBot")
        embed.add_field(name="Original Message: ", value=f"{context}", inline=False)
        embed.set_footer(text="Coded by: PaliKai :)")
        await ctx.send(f"Here you go {ctx.author.mention} !")
        await ctx.send(embed=embed)

    @commands.command(aliases=["cringe"])
    async def joke(self, ctx):
        """Sends a random horrible joke"""
        jokes = ["Why don’t oysters donate to charity? Because they’re shellfish.",
        "What does a baby computer call its father? Data.",
        "What did the custodian say when he jumped out of the closet? 'Supplies!'",
        "Why are colds bad criminals? Because they’re easy to catch.",
        "How does a penguin build its house? Igloos it together.",
        "Which knight invented King Arthur’s Round Table? Sir Cumference.",
        "What do sprinters eat before a race? Nothing. They fast.",
        "What do you call a fly without wings? A walk!",
        "What happens when you witness a ship wreck? You let it sink in.",
        "How can you find Will Smith in the snow? Follow the fresh prints.",
        "What does a clock do when it’s hungry? It goes back four seconds.",
        "What’s the easiest way to make a glow worm happy? Cut off its tail—it’ll be delighted!",
        "What do you call a belt made of watches? A waist of time!",
        "Why did Adele cross the road? To say hello from the other side!",
        "What’s the best way to carve wood? Whittle by whittle.",
        "What did the teacher do with the student’s report on cheese? She grated it.",
        "What’s the difference between a piano and a fish? You can tune a piano, but you can’t tuna fish.",
        "What did the pirate say on his 80th birthday? 'Aye, matey!'",
        "How do you organize an astronomer’s party? You planet.",
        "What’s the action like at a circus? In-tents.",
        "Why did the scarecrow get promoted? Because he was outstanding in his field.",
        "Why does Snoop Dogg carry an umbrella? Fo’ drizzle.",
        "What do you call a pony with a sore throat? A little hoarse.",
        "What do you call a fish with no eye? Fsh.",
        "What do you call a boomerang that doesn’t come back? A stick!",
        "What kind of car does an egg drive? A Yolkswagen.",
        "What do you call a factory that sells generally decent goods? A satisfactory.",
        "Why was 6 afraid of 7? Because 7 ate 9.",
        "Why should you never eat a clock? Because it’s too time consuming.",
        "What should a sick bird do? Get tweetment.",
        "I want a job cleaning mirrors. It’s something I can really see myself doing.",
        "What grades did the pirate get on his report card? Seven Cs.",
        "How do you make a tissue dance? Put a little boogie in it.",
        "How did Ebenezer Scrooge win the football game? The ghost of Christmas passed!",
        "Did you hear about the mediocre restaurant on the moon? It has great food but no atmosphere.",
        "What kinds of pictures do hermit crabs take? Shellfies.",
        "What do you get a man with the heart of a lion? A lifetime ban from the zoo.",
        "What do you call a person with a briefcase in a tree? A branch manager.",
        "Why did the baby cookie cry? Because its mother was a wafer so long.",
        "What’s the difference between an alligator and a crocodile? One you’ll see later, the other you’ll see in a while.",
        "When is a door not really a door? When it’s really ajar.",
        "What do you do when you see a spaceman? Park in it, man.",
        "Why do you never see elephants hiding in trees? Because they’re so good at it!",
        "Did you hear about the claustrophobic astronaut? Poor guy really needed some space.",
        "What’s the No. 1 cause of divorce? Marriage!"]
        await ctx.send(f'{random.choice(jokes)}')

    

def setup(bot):
    bot.add_cog(Fun(bot))




