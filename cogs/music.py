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
import validators
import pafy

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
        else:
            voice_channel = ctx.author.voice.channel

            if ctx.voice_client is None:
                gif = await ctx.send("https://c.tenor.com/_BOcFSneKjwAAAAM/tenten-summoning.gif")
                await asyncio.sleep(1)
                await gif.delete()
                await voice_channel.connect()
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
            if not ctx.voice_client:
                voice_channel = ctx.author.voice.channel
                voice = await voice_channel.connect()
            else:
                voice = ctx.voice_client

            if ctx.voice_client.is_playing():
                await ctx.send("Please wait till the current song gets over or Stop it. Queue Function coming soon (savio plez)")
            else:
                searching = discord.Embed(
                    title="Searching", description=f"{arg}\n\nRequested by: {ctx.author.mention}", color=discord.Color.from_rgb(3, 252, 252))

                searching.set_thumbnail(url=self.client.user.avatar_url)

                serchbed = await ctx.send(embed=searching)

                valid = validators.url(arg)
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

                vid = pafy.new(url)
                brr = vid.title
                thumb_url = vid.thumb
                dur = vid.duration

                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    if valid:
                        url3 = arg
                        video = pafy.new(url3)
                        url = url3
                        thumb_url = video.thumb
                        brr = video.title
                        dur = video.duration

                    info = ydl.extract_info(url, download=False)
                    url2 = info["formats"][0]["url"]

                    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)

                    playing = discord.Embed(
                        title="Now Playing", description=f"🎶[{brr}]({url})\n`[00:00:00/{dur}]`\n\nRequested by: {ctx.author.mention}", color=discord.Color.from_rgb(3, 252, 252))

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
