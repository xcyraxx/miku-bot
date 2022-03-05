"""
Music command script for Miku

Main contributors:
    @savioxavier, @xcyraxx, @UnderdriveAssassin
"""


import os
from async_timeout import timeout
import asyncio
from numpy import random
from utils import ytutil, logutil
import discord
from discord.ext import commands
from discord.ext.commands import Cog, BucketType
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from lyricsgenius import Genius
import itertools


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
        self.queue = []
        self.vc = ""
        self.current_song = []
        self.genius = Genius(os.environ.get("GENIUS_TOKEN"))

    @Cog.listener()
    async def on_ready(self):
        self.tick = self.client.get_emoji(930836902347694081)
        logger.info("Music up!")

    async def play_music(self, ctx):
        self.is_playing = True

        source = self.queue[0].source
        self.current_song = self.queue.pop(0)

        self.vc.play(source, after=lambda e: self.play_next())
        await ctx.send(embed=self.current_song.create_play())

    def play_next(self):
        if len(self.queue) > 0:
            self.is_playing = True

            self.current_song = self.queue[0]
            source = self.queue[0].source
            self.vc.play(source, after=lambda e: self.play_next())
            logger.info(f"Playing {self.current_song.title}")
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

        if not auth.voice:
            await ctx.reply("You're not connected to a Voice Channel.")
            return
        if ctx.voice_client is None:
            self.vc = await auth.voice.channel.connect()
            logger.info(f"{auth} made Miku join {auth.voice.channel}")
            await ctx.reply(f"`Connected to `<#{auth.voice.channel.id}>")
        else:
            self.vc = await ctx.voice_client.move_to(auth.voice.channel)
            logger.info(
                f"{auth} made Miku switch to {auth.voice.channel}")
            await ctx.reply(f"`Switched to `<#{auth.voice.channel.id}>")

    @cog_ext.cog_slash(name="leave", description="Disconnects the bot.", guild_ids=__GUILD_ID__)
    async def _slash_leave(self, ctx):
        "Leave a voice if the bot is connected to a Voice Channel, else raise error if it isn't"

        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            logger.info(f"{ctx.author} made Miku leave")
            await ctx.reply(f"{self.tick}")
        else:
            await ctx.reply("I'm not connected to Voice Channel.")

    @commands.command(name="leave", aliases=[""], help="Disconnects the bot.")
    async def _reg_leave(self, ctx):
        "Disconnects the bot."
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            logger.info(f"{ctx.author} made Miku leave")
            await ctx.reply("Disconnected from Voice Channel.")
        else:
            await ctx.reply("I'm not connected to a voice channel.")
    # FIX: Low quality code

    @cog_ext.cog_slash(name="play", description="Play any song by name", guild_ids=__GUILD_ID__)
    async def _slash_play(self, ctx, song_name: str):
        await self._play(ctx, song_name)

    @commands.command(name="play", description="Play any song by name", aliases=["p"])
    @commands.cooldown(1, 5, BucketType.user)
    async def _reg_play(self, ctx, *, song_name: str):
        await self._play(ctx, song_name)

    async def _play(self, ctx, song_name):
        """Play a YouTube video using the youtube_dl library

        Args:
            arg (string, optional): Search query or video URL. Defaults to None.
        """
        if not ctx.voice_client:
            await self._join(ctx)

        embed = ytutil.create_search(ctx, song_name)
        search_embed = await ctx.reply(embed=embed, mention_author=False)
        song = await ytutil.get_data(song_name, ctx)
        self.queue.append(song)
        if not self.vc.is_playing():
            await self.play_music(ctx)
        else:
            await search_embed.edit(embed=song.create_queue())

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
                await ctx.reply("⏸️")
            else:
                await ctx.reply("Nothing is playing")
        else:
            await ctx.reply("I'm not connected to a voice channel.")

    @cog_ext.cog_slash(name="skip", description="Skips the current song.", guild_ids=__GUILD_ID__)
    async def _slash_skip(self, ctx):
        await self._skip(ctx)

    @commands.command(name="skip", aliases=["s"], description="Skips the current song.")
    async def _reg_skip(self, ctx):
        await self._skip(ctx)

    async def _skip(self, ctx):
        if len(self.queue) <= 0:
            await ctx.reply("The Queue is empty")
        else:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            else:
                await ctx.reply(".-. I'm not playing anything~")
                return
            # try to play next in the queue if it exists
            await self.play_music(ctx)
            await ctx.reply("⏩")

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
            await ctx.reply("▶️")
        else:
            await ctx.reply("There isn't anything to resume.")

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
            await ctx.reply("⏹️")
        else:
            await ctx.reply("There isn't anything to stop.")

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
        await ctx.reply("Queue cleared.")

    # queue command
    @cog_ext.cog_slash(name="queue", description="View the current queue.", guild_ids=__GUILD_ID__)
    async def _slash_queue(self, ctx):
        await self._queue(ctx)

    @commands.command(name="queue", aliases=["q"], description="View the current queue.")
    async def _reg_queue(self, ctx):
        await self._queue(ctx)

    async def _queue(self, ctx):
        if len(self.queue) <= 0:
            await ctx.reply("The Queue is empty.")
        else:
            upnext = "\n".join(
                [f"`{i + 1}.` [{song.title}]({song.url}) `[{song.duration}]`" for i,
                 song in enumerate(self.queue)]
            )
            embed = discord.Embed(
                title="Queue",
                color=discord.Color.from_rgb(3, 252, 252)
            )
            embed.add_field(
                name="Current", value=f"[{self.current_song.title}]({self.current_song.url}) `[{self.current_song.duration}]`", inline=False)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(text=f"{len(self.queue)} songs in queue. • use /skip to skip songs") if len(
                self.queue) > 1 else embed.set_footer(text="1 song in queue.")
            embed.add_field(name="Up next", value=upnext)
            await ctx.reply(embed=embed)
            try:
                logger.info(f"{ctx.author} requested the queue")
            except AttributeError:
                logger.info(f"{ctx.message.author.name} requested the queue")

    async def _queue_remove(self, ctx, index: str):
        removed = self.queue.pop(int(index) - 1)
        try:
            logger.info(
                f"{ctx.author} removed {removed.name} from the queue.")
        except AttributeError:
            logger.info(
                f"{ctx.message.author} removed {removed[0]} from the queue.")
        await ctx.reply(f"Removed `{removed.name}` from the queue.")

    @commands.command(name="remove", aliases=["r", "qr"], description="Remove a song from the queue.")
    async def _reg_remove(self, ctx, index: str):
        await self._queue_remove(ctx, index)

    @cog_ext.cog_slash(name="remove", description="Remove a song from the queue.", guild_ids=__GUILD_ID__)
    async def _slash_queue_remove(self, ctx, index: str):
        await self._queue_remove(ctx, index)

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
            await ctx.reply("Couldn't find the song")
            return
        if not song:
            await ctx.reply("Couldn't find the song")
            return

        if song.lyrics is None:
            await ctx.reply("Couldn't find the lyrics for that song")
            return
        # get the lyrics
        lyrics = song.lyrics.replace("EmbedShare URLCopyEmbedCopy", "")
        thumbnail = song.song_art_image_url
        if lyrics is None:
            await ctx.reply("Couldn't find the lyrics")
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
            await ctx.reply(embed=embed)
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
            await ctx.reply(embed=e, mention_author=False)

    @commands.command(name="shuffle", description="Shuffle the queue.")
    async def _reg_shuffle(self, ctx):
        await self._shuffle(ctx)

    @cog_ext.cog_slash(name="shuffle", description="Shuffle the queue.", guild_ids=__GUILD_ID__)
    async def _slash_shuffle(self, ctx):
        await self._shuffle(ctx)

    async def _shuffle(self, ctx):
        random.shuffle(self.queue)
        try:
            logger.info(f"{ctx.author} shuffled the queue.")
        except AttributeError:
            logger.info(f"{ctx.message.author} shuffled the queue.")
        await ctx.reply("Queue shuffled.")

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(f"`Error: Missing required argument {error.param.name}`")
        elif isinstance(error, commands.BadArgument):
            await ctx.reply(f"`{error}`")
        elif isinstance(error, commands.CommandOnCooldown):
            # we dont even have any cooldowns lmaoo
            await ctx.reply(f"`Error: Command on cooldown. Try again in {round(error.retry_after, 2)} seconds`")
        else:
            await ctx.reply(f"`{error}`")
            logger.error(f"{ctx.author} caused an error: {error}")


def setup(bot):
    "Setup command for the bot"

    bot.add_cog(Music(bot))
