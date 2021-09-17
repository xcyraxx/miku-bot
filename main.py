"""
Master script for Miku

Main contributors:
    @savioxavier, @xcyraxx, @Undrivesure
    Assassin
"""

from logging import info
import os
import discord
from discord.enums import Status
from discord.ext import commands
from dotenv import load_dotenv
from calendar import timegm
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option


load_dotenv()
TOKEN = os.environ.get("TOKEN")

__version__ = "1.2.0"
__GUILD_ID__ = 846609621429780520

custom_prefixes = {}
default_prefixes = [">>"]


intents = discord.Intents.default()
intents.members = True


async def determine_prefix(bot, message):
    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes

activity = discord.Game(name=">>help")
client = commands.Bot(command_prefix=determine_prefix,
                      case_insensitive=True,
                      activity=activity,
                      intents=intents,
                      help_command=None,
                      status=Status.idle
                      )
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    "Function to determine what commands are to be if bot is connected to Discord"

    print("Miku Online.")
    STDOUT_CHANNEL = await client.fetch_channel(885979416369438751)
    await STDOUT_CHANNEL.send(f"Prototype {__version__} Online.")


@client.command()
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    """Function to change bot prefix from the default

    Args:
        prefixes (str, optional): Prefix to be used. Defaults to "".
    """
    custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes
    await ctx.send("Prefixes set!")


@slash.slash(name="shutdown", description="Owner Only", guild_ids=[__GUILD_ID__])
@commands.is_owner()
async def shutdown(ctx):
    "Terminates bot process"

    STDOUT_CHANNEL = await client.fetch_channel(885979416369438751)
    await STDOUT_CHANNEL.send(f"Prototype {__version__} Offline.")
    await ctx.send("Shutting Down..")
    print("Shutting Down...")
    await client.close()

MAIN_HELP = "**Miku** - The only music bot you'll ever need!"

MUSIC_HELP = """
**`summon`**: 
    Connect the bot your current Voice Channel.

**`play <song_name | url>`**: 
    Play a song from YouTube given a search term or URL.

**`stop`**: 
    Stop playing the song.

**`pause`**: 
    Pause the song currently playing.

**`resume`**: 
    Resume playing the song.
"""

OTHER_HELP = """
**`botinfo`**: 
    Some info about the Bot.
"""


#help command
# @client.command(name="help", description="List commands")
# async def command_help(ctx):
#     "Main help command for the bot"
#     bot_help = discord.Embed(
#         title="Miku Help",
#         description=MAIN_HELP,
#         color=discord.Color.from_rgb(3, 252, 252))
#     bot_help.set_thumbnail(url=client.user.avatar_url)
#     bot_help.add_field(name="Music Commands",
#                        value=MUSIC_HELP, inline=False)
#     bot_help.add_field(name="Other", value=OTHER_HELP, inline=True)
#     await ctx.send(embed=bot_help)

@slash.slash(
    name="help",
    description="Displays the commands and their descriptions.",
    guild_ids=[__GUILD_ID__]
)
async def help(ctx:SlashContext):
    bot_help = discord.Embed(
        title="Miku Help",
        description=MAIN_HELP,
        color=discord.Color.from_rgb(3, 252, 252))
    bot_help.set_thumbnail(url=client.user.avatar_url)
    bot_help.add_field(name="Music Commands",
                       value=MUSIC_HELP, inline=False)
    bot_help.add_field(name="Other", value=OTHER_HELP, inline=True)
    await ctx.send(embed=bot_help)


client.load_extension("cogs.music")
client.load_extension("cogs.meta")
client.run(TOKEN)
