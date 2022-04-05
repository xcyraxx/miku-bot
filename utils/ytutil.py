"""
Ytdl utils 
"""

import re
import urllib
from datetime import timedelta
from typing import Text

import discord
import validators
import youtube_dl


class YTDLSource(discord.PCMVolumeTransformer):
    global YTDL_OPTIONS
    YTDL_OPTIONS = {
        "format": "bestaudio/best",
        "extractaudio": True,
        "audioformat": "mp3",
        "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
    }
    global FFMPEG_OPTIONS
    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }
    global ytdl
    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)


class Song(object):
    "Song object"

    def __init__(
        self,
        source,
        title: Text,
        url: Text,
        duration: Text,
        thumbnail: Text,
        requester: Text,
    ):
        self.source = source
        self.title = title
        self.url = url
        self.duration = duration
        self.thumbnail = thumbnail
        self.requester = requester

    def create_play(self):
        return self.create_ytutil_discord_embed(
            "Now Playing", "🎶", "\n`[00:00:00/", "]`\n\nRequested by: "
        )

    def create_queue(self):
        return self.create_ytutil_discord_embed(
            "Added to Queue", "**", "**\n`", "`\nRequested by "
        )

    def create_ytutil_discord_embed(self, title, arg1, arg2, arg3):
        playing = discord.Embed(
            title=title,
            description=f"{arg1}{self.title}{arg2}{self.duration}{arg3}{self.requester.mention}",
            color=discord.Color.from_rgb(3, 252, 252),
        )

        playing.set_thumbnail(url=self.thumbnail)
        return playing


def create_search(ctx, song_name):
    try:
        auth = ctx.author
    except AttributeError:
        auth = ctx.message.author
    searching = discord.Embed(
        title="Searching",
        description=f"{song_name}\n\nRequested by: " + auth.mention,
        color=discord.Color.from_rgb(3, 252, 252),
    )
    searching.set_thumbnail(
        url="https://media.discordapp.net/attachments/884694080708300831/899203305140518962/mikuload.gif?width=469&height=469"
    )
    return searching


async def get_data(song_name, ctx):

    query_string = urllib.parse.urlencode({"search_query": song_name})

    htm_content = urllib.request.urlopen(
        f"https://www.youtube.com/results?{query_string}"
    )

    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())

    search_url = f"http://www.youtube.com/watch?v={search_results[1]}"
    valid = validators.url(song_name)
    with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ytdl:
        if valid:
            search_url = song_name

        info = ytdl.extract_info(search_url, download=False)
        video_url = info["formats"][0]["url"]
        title = info["title"]
        duration = timedelta(seconds=info["duration"])
        thumbnail_url = info["thumbnail"]
        author = ctx.author
        source = await discord.FFmpegOpusAudio.from_probe(video_url, **FFMPEG_OPTIONS)
        return Song(source, title, video_url, duration, thumbnail_url, author)
