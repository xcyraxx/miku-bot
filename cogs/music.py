"""
Music command script for Miku

Main contributors:
    @savioxavier, @xcyraxx, @UndriveAssassin
"""

import urllib.request
import urllib.parse
import asyncio
import re
import os
import discord
from discord.ext import commands
from discord.ext.commands import Cog
import youtube_dl
from bs4 import BeautifulSoup
import requests
import pafy

EMBED_COLOR = os.environ.get("EMBED_COLOR")
PREFIX = os.environ.get("PREFIX")


class Music(commands.Cog):
    """Main class for the Music command

    Args:
        commands (string): Command
    """

    def __init__(self, client):
        "Init function for Discord client"

        self.client = client

    @Cog.listener()
    async def on_ready(self):
        "Function to determine what commands are to be if bot is connected to Discord"

        print("Music up!")

    @commands.command(name="summon", aliases=("join", "kuchiyose"), description="Connects the bot to voice channel.")
    async def command_join(self, ctx):
        "Join a Voice Channel if the author is present in one, else raise error if they aren't"

        if ctx.author.voice is None:
            await ctx.send("You're not connected to a Voice Channel.")

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            gif = await ctx.send("https://c.tenor.com/_BOcFSneKjwAAAAM/tenten-summoning.gif")
            await asyncio.sleep(1)
            await gif.delete()
            await voice_channel.connect()
            await ctx.guild.change_voice_state(channel=voice_channel, self_deaf=True)
            await ctx.send("Hi there!")
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(name="leave", aliases=("exit", "kill"), description="Disconnects the bot from channel.")
    async def command_leave(self, ctx):
        "Leave a voice if the bot is connected to a Voice Channel, else raise error if it isn't"

        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("See ya!")
        else:
            await ctx.send("I'm not connected to Voice Channel.")

    @commands.command(name="play", description="Play any song by name. Usage: >>play song name")
    async def command_play(self, ctx, *, arg=None):
        """Play a YouTube video using the youtube_dl library

        Args:
            arg (string, optional): Search query or video URL. Defaults to None.
        """
        # TODO: FIX : Too many local variables

        if arg:
            urls = re.findall(
                "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", arg.lower())

            if not ctx.voice_client:
                voice_channel = ctx.author.voice.channel
                voice = await voice_channel.connect()
                await ctx.guild.change_voice_state(channel=voice_channel, self_deaf=True)
            else:
                voice = ctx.voice_client

            searching = discord.Embed(
                title="Searching", description=f"Now searching for `{arg}`", color=discord.Color.from_rgb(3, 252, 252))

            searching.set_thumbnail(url=self.client.user.avatar_url)

            searching.set_footer(
                text=f"Requested By {ctx.author.display_name}")

            serchbed = await ctx.send(embed=searching)

            FFMPEG_OPTIONS = {
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}

            YDL_OPTIONS = {}

            query_string = urllib.parse.urlencode({
                "search_query": arg
            })

            htm_content = urllib.request.urlopen(
                "https://www.youtube.com/results?" + query_string
            )

            search_results = re.findall(
                r"watch\?v=(\S{11})", htm_content.read().decode())

            url = f"http://www.youtube.com/watch?v={search_results[1]}"

            req = requests.get(url)
            soup = BeautifulSoup(req.text, "html.parser")
            title = soup.find("meta", property="og:title")
            brr = title["content"] if title else "No meta title given"

            thumb_url = f"https://img.youtube.com/vi/{search_results[1]}/maxresdefault.jpg"

            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                if arg in urls:
                    print(arg)

                    url3 = arg
                    video = pafy.new(url3)
                    url = url3
                    thumb_url = video.thumb
                    brr = video.title

                info = ydl.extract_info(url, download=False)
                url2 = info["formats"][0]["url"]

                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

                playing = discord.Embed(
                    title="Playing", description=f"🎶Now playing `{brr}`", color=discord.Color.from_rgb(3, 252, 252))

                playing.set_thumbnail(url=thumb_url)

                voice.play(source)

                await serchbed.edit(embed=playing)

        else:
            await ctx.send(f"Provide a name or a link to play the song. Usage: `{PREFIX}play song name`")

    @commands.command()
    async def pause(self, ctx):
        "Pause music"

        if ctx.voice_client:
            ctx.voice_client.pause()
            await ctx.send("Paused ⏸️")
        else:
            await ctx.send("There isn't anything to pause.")

    @commands.command()
    async def resume(self, ctx):
        "Resume music"

        if ctx.voice_client:
            ctx.voice_client.resume()
            await ctx.send("Resume ▶️")
        else:
            await ctx.send("There isn't anything to resume.")

    @commands.command()
    async def stop(self, ctx):
        "Stop music"

        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.send("Stopped ⏹️")
        else:
            await ctx.send("There isn't anything to stop.")

    # TODO: Add queues using database and Flask server request - I'll do it, I swear!
    @commands.command(name="queue", description="Displays the current queue.")
    async def command_queue(self, ctx):
        "Displays current song queue/list"
        queue = []
        for i in queue:
            print(i)


def setup(bot):
    "Setup command for the bot"
    bot.add_cog(Music(bot))
