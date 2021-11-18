import asyncio

import discord
import youtube_dl
import discord.voice_client
from discord.ext import commands

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ""


ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "192.168.1.45",  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ctx.author.voice.channel)

        await ctx.author.voice.channel.connect()


    @commands.command()
    async def play(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )

        embed=discord.Embed(title="Now Playing:", description=f"{player.title}", color=0xff00ff)
        embed.set_author(name="RaiseBot")
        embed.add_field(name="Requested by: ", value=f"{ctx.author}", inline=False)
        embed.set_footer(text="Coded by: iamu")
        await ctx.send(embed=embed)

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command(aliases=['iamufavs','fav'])
    async def favs(self,ctx):
        """Literally just sends a list of iamu's favorite songs"""
        fav_music = ["https://www.youtube.com/watch?v=NcXsK_u4ixI - I cant go on without you",
        "https://www.youtube.com/watch?v=fIdnpjceg9A - Aint no sunshine (Bill Withers)",
        "https://www.youtube.com/watch?v=oyJ_yEFCm7E - Enemy",
        "https://www.youtube.com/watch?v=UZsHXhg9e7M - Desperado (Remix)",
        "https://www.youtube.com/watch?v=CSD2J8yaMmM - Ms. Jackson",
        "https://www.youtube.com/watch?v=J4KIyp9iBMg - Bottom of the bottle",
        "https://www.youtube.com/watch?v=doRUhDIB29s - Hallucinogenics",
        "https://www.youtube.com/watch?v=ev-bR9ii7Gs - Lydia",
        "https://www.youtube.com/watch?v=xLnhtTlwjak - Hellboy",
        "https://www.youtube.com/watch?v=n-SIyuIyh7E - Past the castle walls",
        "https://www.youtube.com/watch?v=s1-0lt7b-78 - ANTARCTICA",
        "https://www.youtube.com/watch?v=TZUz9Dm9N-Y - Mary Jane (KAAN)",
        "https://www.youtube.com/watch?v=89q3dxdIkIQ&t=0s - Clockwork 4",
        "https://www.youtube.com/watch?v=P4MiC67seUY - Sorry you're not a winner",
        "https://www.youtube.com/watch?v=DoCm3OWQGjQ - frailty"]
        fav_music_str = ""
        for i in fav_music:
           fav_music_str = fav_music_str + i + '\n'
        embed=discord.Embed(title="Iamu's Fav Songs:", description=f"{fav_music_str}", color=0xff00ff)
        embed.set_author(name="RaiseBot")
        embed.set_footer(text="Coded by: iamu")
        await ctx.send(embed=embed)

    @commands.command()
    async def nice(self, ctx):
        """*click*... noice."""
        ch = ctx.author.voice.channel
        #https://www.youtube.com/watch?v=UBX8MWYel3s
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ch)
        await ch.connect()
        async with ctx.typing():
            player = await YTDLSource.from_url('https://www.youtube.com/watch?v=UBX8MWYel3s', loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )
        await asyncio.sleep(5)
        await ctx.voice_client.disconnect()

    @commands.command(aliases=['poop'])
    async def plsdontusethiscommand(self, ctx):
        """DO NOT USE THIS COMMAND IT IS TERRIBLE"""
        #https://youtu.be/GWNwwuoc4Ro
        ch = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ch)
        await ch.connect()
        async with ctx.typing():
            player = await YTDLSource.from_url('https://youtu.be/GWNwwuoc4Ro', loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )
        await asyncio.sleep(180)
        await ctx.voice_client.disconnect()

    @commands.command(aliases=['goobity'])
    async def rugrats(self, ctx):
        #https://www.youtube.com/watch?v=4GicJVYQvcg
        """Goobity Gobbity"""
        ch = ctx.author.voice.channel
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(ch)
        await ch.connect()
        async with ctx.typing():
            player = await YTDLSource.from_url('https://www.youtube.com/watch?v=4GicJVYQvcg', loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player, after=lambda e: print(f"Player error: {e}") if e else None
            )
        await asyncio.sleep(8)
        await ctx.voice_client.disconnect()


def setup(bot):
    bot.add_cog(Music(bot))