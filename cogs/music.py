"""
Music command script for Miku

Main contributors:
    @savioxavier, @xcyraxx, @UnderdriveAssassin
"""

import datetime as dt
import os
import re
import urllib.parse
import urllib.request
from typing import Text

import discord
import pafy
import requests
import validators
import youtube_dl
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands.core import command
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
from lyricsgenius import Genius
from validators.url import url

from utils import logutil

__GUILD_ID__ = [846609621429780520, 893122121805496371]
PREFIX = os.environ.get("PREFIX")

logger = logutil.init()


class Music(commands.Cog):
    """Main class for the Music command

    Args:
        commands (string): Command
    """

    def __init__(self, client):
        "Init function for Discord client"

        self.client = client
        self.FFMPEG_OPTIONS = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
        self.queue = []
        self.vc = ""
        self.current_song = []
        self.GENIUS_TOKEN = "BZDhGkSxGrYjp4ljfm4NaTbWPe15Ll3lHVlSwFeKuOxj-YdmwLTj4C6j8ULojoh6"
        self.genius = Genius(self.GENIUS_TOKEN)

    @Cog.listener()
    async def on_ready(self):
        "Function to determine what commands are to be if bot is connected to Discord"
        self.tick = self.client.get_emoji(930836902347694081)
        logger.info("Music up!")

    def play_next(self):
        if len(self.queue) > 0:
            self.is_playing = True

            self.current_song = self.queue[0]
            source = self.queue[0][1]
            self.vc.play(source, after=lambda e: self.play_next())

        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self):
        if len(self.queue) > 0:
            self.is_playing = True

            self.current_song = self.queue[0]
            source = self.queue[0][1]
            self.queue.pop(0)

            self.vc.play(source, after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @cog_ext.cog_slash(name="join", description="Join your current voice channel", guild_ids=__GUILD_ID__)
    async def _slash_join(self, ctx):
        await self._join(ctx)

    @commands.command(name="join", aliases=["j"], help="Join your current voice channel")
    async def _reg_join(self, ctx):
        "Join your current voice channel"
        await self._join(ctx)

    async def _join(self, ctx):
        "Join a Voice Channel if the author is present in one, else raise error if they aren't"
        try:
            auth = ctx.author
        except AttributeError:
            auth = ctx.message.author

        logger.info(f"{auth} executed join")

        if auth.voice is None:
            await ctx.send("You're not connected to a Voice Channel.")
        else:
            voice_channel = auth.voice.channel

            if ctx.voice_client is None:
                self.vc = await voice_channel.connect()
                logger.info(f"{auth} made Miku join {voice_channel}")
                await ctx.send(f"`Connected to `<#{auth.voice.channel.id}>")
            else:
                self.vc = await ctx.voice_client.move_to(voice_channel)
                logger.info(
                    f"{auth} made Miku switch to {voice_channel}")
                await ctx.send(f"`Switched to `<#{auth.voice.channel.id}>")

    @cog_ext.cog_slash(name="leave", description="Disconnects the bot.", guild_ids=__GUILD_ID__)
    async def _slash_leave(self, ctx):
        "Leave a voice if the bot is connected to a Voice Channel, else raise error if it isn't"

        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            logger.info(f"{ctx.author} made Miku leave")
            await ctx.send(f"{self.tick}")
        else:
            await ctx.send("I'm not connected to Voice Channel.")

    @commands.command(name="leave", aliases=[""], help="Disconnects the bot.")
    async def _reg_leave(self, ctx):
        "Disconnects the bot."
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            logger.info(f"{ctx.author} made Miku leave")
            await ctx.send("Disconnected from Voice Channel.")
        else:
            await ctx.send("I'm not connected to a voice channel.")
    # FIX: Low quality code

    @cog_ext.cog_slash(name="play", description="Play any song by name", guild_ids=__GUILD_ID__)
    async def _slash_play(self, ctx, song_name: str):
        await self._play(ctx, song_name)

    @commands.command(name="play", description="Play any song by name", aliases=["p"])
    async def _reg_play(self, ctx, *, song_name: str):
        await self._play(ctx, song_name)

    async def _play(self, ctx, song_name):
        """Play a YouTube video using the youtube_dl library

        Args:
            arg (string, optional): Search query or video URL. Defaults to None.
        """
        # TODO: FIX : Too many local variables

        if ctx.author.voice is None:
            await ctx.send("You're not connected to a Voice Channel.")

        elif song_name:
            a = "gud"
            if ctx.voice_client:
                self.vc = ctx.voice_client

            elif not ctx.author.voice:
                a = "bad"  # bad way i know
            else:
                voice_channel = ctx.author.voice.channel
                logger.info(f"{ctx.author} made Miku join {voice_channel}")
                self.vc = await voice_channel.connect()
            if a != "bad":
                searching = discord.Embed(
                    title="Searching", description=f"{song_name}\n\nRequested by: {ctx.author.mention}", color=discord.Color.from_rgb(3, 252, 252))

                searching.set_thumbnail(
                    url="https://media.discordapp.net/attachments/884694080708300831/899203305140518962/mikuload.gif?width=469&height=469")

                serchbed = await ctx.send(embed=searching)

                valid = validators.url(song_name)

                YDL_OPTIONS = {}

                query_string = urllib.parse.urlencode({
                    "search_query": song_name
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
                auth = ctx.author.mention

                with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                    if valid:
                        url3 = song_name
                        video = pafy.new(url3)
                        url = url3
                        thumb_url = video.thumb
                        brr = video.title
                        dur = video.duration
                        auth = ctx.author.mention

                    info = ydl.extract_info(url, download=False)
                    url2 = info["formats"][0]["url"]

                    source = await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS)

                    if ctx.voice_client.is_playing():
                        self.queue.append(
                            [brr, source, thumb_url, dur, auth, url])
                        queued = discord.Embed(
                            title="Added to Queue",
                            description=f"**{brr}**\n`{dur}`\nRequested by {ctx.author.mention}",
                            color=discord.Color.from_rgb(3, 252, 252),
                            timestamp=ctx.message.created_at
                        )
                        queued.set_thumbnail(url=thumb_url)
                        logger.info(f"{ctx.author} added '{brr}' to queue")
                        await serchbed.edit(embed=queued)
                    else:
                        playing = discord.Embed(
                            title="Now Playing", description=f"🎶{brr}\n`[00:00:00/{dur}]`\n\nRequested by: {ctx.author.mention}", color=discord.Color.from_rgb(3, 252, 252),
                            timestamp=ctx.message.created_at)

                        playing.set_thumbnail(url=thumb_url)

                        self.vc.play(source)
                        self.current_song = [
                            brr, source, thumb_url, dur, auth, url]

                        await serchbed.edit(embed=playing)
                        logger.info(f"{ctx.author} played '{brr}'")
            else:
                await ctx.send("You're not connected to a voice channel.")
        else:
            await ctx.send(
                'Provide a name or a link to play the song. Usage: `/play song name`'
            )

    @cog_ext.cog_slash(name="pause", description="Pause the current song.", guild_ids=__GUILD_ID__)
    async def _slash_pause(self, ctx):
        await self._pause(ctx)

    @commands.command(name="pause", description="Pause the current song.")
    async def _reg_pause(self, ctx):
        await self._pause(ctx)

    async def _pause(self, ctx):
        "Pause music"
        if ctx.voice_client:
            if ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                try:
                    logger.info(f"{ctx.author} paused the music.")
                except AttributeError:
                    logger.info(f"{ctx.message.author} paused the music.")
                await ctx.send("Paused ⏸️")
            else:
                await ctx.send("Nothing is playing")
        else:
            await ctx.send("I'm not connected to a voice channel.")

    @cog_ext.cog_slash(name="skip", description="Skips the current song.", guild_ids=__GUILD_ID__)
    async def _slash_skip(self, ctx):
        await self._skip(ctx)

    @commands.command(name="skip", aliases=["s"], description="Skips the current song.")
    async def _reg_skip(self, ctx):
        await self._skip(ctx)

    async def _skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        else:
            await ctx.send(".-. I'm not playing anything~")
        if len(self.queue) <= 0:
            await ctx.send("The Queue is empty")
        else:
            brr = self.queue[0][0]
            dur = self.queue[0][3]
            thumb_url = self.queue[0][2]
            # try to play next in the queue if it exists
            await self.play_music()
            try:
                auth = ctx.author.mention
            except AttributeError:
                auth = ctx.message.author.mention
            new = discord.Embed(
                title="Now Playing",
                description=f"🎶{brr}\n`[00:00:00/{dur}]`\n\nRequested by: {auth}",
                color=discord.Color.from_rgb(3, 252, 252))
            new.set_thumbnail(url=thumb_url)
            logger.info(f"{auth} skipped the music.")
            await ctx.send("Skipped⏩", embed=new)

    @cog_ext.cog_slash(name="resume", description="Resume the current song.", guild_ids=__GUILD_ID__)
    async def _slash_resume(self, ctx):
        await self._resume(ctx)

    @commands.command(name="resume", aliases=["unpause, naruto"], description="Resume the current song.", guild_ids=__GUILD_ID__)
    async def _reg_resume(self, ctx):
        await self._resume(ctx)

    async def _resume(self, ctx):
        "Resume music"

        if ctx.voice_client:
            ctx.voice_client.resume()
            try:
                logger.info(f"{ctx.author} resumed the music.")
            except:
                logger.info(f"{ctx.message.author} resumed the music.")
            await ctx.send("Resumed ▶️")
        else:
            await ctx.send("There isn't anything to resume.")

    @cog_ext.cog_slash(name="stop", description="Stop the current song.", guild_ids=__GUILD_ID__)
    async def _slash_stop(self, ctx):
        await self._stop(ctx)

    @commands.command(name="stop", aliases=["sasuke"], description="Stop the current song.")
    async def _reg_stop(self, ctx):
        await self._stop(ctx)

    async def _stop(self, ctx):
        "Stop music"

        if ctx.voice_client:
            ctx.voice_client.stop()
            try:
                logger.info(f"{ctx.author} stopped the music.")
            except:
                logger.info(f"{ctx.message.author} stopped the music.")
            await ctx.send("Stopped ⏹️")
        else:
            await ctx.send("There isn't anything to stop.")

    @cog_ext.cog_slash(name="clear", description="Clear the current queue.", guild_ids=__GUILD_ID__)
    async def _slash_clear(self, ctx):
        await self._clear(ctx)

    @commands.command(name="clear", aliases=["clr"], description="Clear the current queue.")
    async def _reg_clear(self, ctx):
        await self._clear(ctx)

    async def _clear(self, ctx):
        self.queue.clear()
        try:
            logger.info(f"{ctx.author} cleared the queue.")
        except AttributeError:
            logger.info(f"{ctx.message.author} cleared the queue.")
        await ctx.send("Queue cleared.")

    # queue command
    @cog_ext.cog_slash(name="queue", description="View the current queue.", guild_ids=__GUILD_ID__)
    async def _slash_queue(self, ctx):
        await self._queue(ctx)

    @commands.command(name="queue", aliases=["q"], description="View the current queue.")
    async def _reg_queue(self, ctx):
        await self._queue(ctx)

    async def _queue(self, ctx):
        if len(self.queue) <= 0:
            await ctx.send("The Queue is empty.")
        else:
            embed = discord.Embed(
                title="Queue",
                color=discord.Color.from_rgb(3, 252, 252)
            )
            embed.add_field(
                name="Current", value=f"[{self.current_song[0]}]({self.current_song[5]}) `{self.current_song[3]}`", inline=False)
            embed.add_field(name="Up next", value="\n".join(
                [f"`{i + 1}.` [{song[0]}]({song[5]}) `[{song[3]}]`" for i,
                 song in enumerate(self.queue)]
            ))
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(
                text=f"{len(self.queue)} songs in queue. • use /skip to skip songs")
            try:
                logger.info(f"{ctx.author} requested the queue")
            except AttributeError:
                logger.info(f"{ctx.message.author.name} requested the queue")
            await ctx.send(embed=embed)

    # command to get lyrics from genius
    @cog_ext.cog_slash(name="lyrics", description="Get the lyrics of a song.", guild_ids=__GUILD_ID__,
                       options=[
                           create_option(
                               name="song",
                               description="The song to get the lyrics of.",
                               option_type=3,
                               required=False
                           )
                       ]
                       )
    async def _slash_lyric(self, ctx, song):
        await self._lyrics(ctx, song)

    @commands.command(name="lyrics", aliases=["l"],)
    async def _reg_lyrics(self, ctx, *, song):
        await self._lyrics(ctx, song)

    async def _lyrics(self, ctx, song):
        # get the song from genius
        try:
            song = self.genius.search_song(song)
        except:
            await ctx.send("Couldn't find the song")
            return
        if not song:
            await ctx.send("Couldn't find the song")
            return

        if song.lyrics is None:
            await ctx.send("Couldn't find the lyrics for that song")
            return
        # get the lyrics
        lyrics = song.lyrics.replace("EmbedShare URLCopyEmbedCopy", "")
        thumbnail = song.song_art_image_url
        if lyrics is None:
            await ctx.send("Couldn't find the lyrics")
            return

        if len(lyrics) > 2000:
            s1 = lyrics[:len(lyrics)//2]
            embed = discord.Embed(
                title=f"Lyrics for {song.full_title}",
                description=f"{s1}\n\n[Full lyrics here]({song.url})",
                color=discord.Color.from_rgb(3, 252, 252)
            )
            embed.set_thumbnail(url=thumbnail)
            embed.set_footer(
                text=f"Requested by {ctx.author.name} • Artist: {song.artist}")
            logger.info(
                f"{ctx.author} requested the lyrics for '{song.full_title}'")
            await ctx.send(embed=embed)
        else:
            e = discord.Embed(
                title=f"Lyrics for {song.full_title}", description=lyrics, color=discord.Color.from_rgb(3, 252, 252)
            )
            e.set_thumbnail(url=thumbnail)
            try:
                e.set_footer(
                    text=f"Requested by {ctx.author.name} • Artist: {song.artist}")
            except AttributeError:
                e.set_footer(
                    text=f"Requested by {ctx.message.author.name} • Artist: {song.artist}")
            logger.info(
                f"{ctx.author} requested the lyrics for '{song.full_title}'")
            await ctx.send(embed=e)

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"error: Missing required argument {error.param.name}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.CommandOnCooldown):
            # we dont even have any cooldowns lmaoo
            await ctx.send(f"Command on cool down. Try again in {error.retry_after}seconds")
        else:
            await ctx.send(error)


def setup(bot):
    "Setup command for the bot"

    bot.add_cog(Music(bot))
