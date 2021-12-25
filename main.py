"""
Master script for Miku

Main contributors:
    @savioxavier, @xcyraxx, @UndriveAssassin
    Assassin
"""
# ol(

import os
from gc import set_threshold
import json
import discord
from discord import guild
from discord.enums import Status
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.converter import clean_content
from discord_slash import SlashCommand
import discord_slash
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import (ComponentContext,
                                                   create_actionrow,
                                                   create_select,
                                                   create_select_option,
                                                   wait_for_component)
from dotenv import load_dotenv

from utils import logutil
load_dotenv()

TOKEN = os.environ.get("TOKEN")
__GUILD_ID__ = []
for i in open("utils/guilds.txt", "r").read().split("\n"):
    if i:
        __GUILD_ID__.append(int(i.replace("'", "")))

__version__ = "1.3.0"

custom_prefixes = {}
default_prefixes = [">>"]


intents = discord.Intents.default()
intents.members = True


async def determine_prefix(bot, message):
    "Determine prefix for the bot"

    guild = message.guild
    if guild:
        return custom_prefixes.get(guild.id, default_prefixes)
    else:
        return default_prefixes

logger = logutil.init()
logger.warning(
    f"Debug Mode is {logutil.DEBUG}. discord.py Debug Mode is {logutil.DEBUG_DISCORD}")

logger.info("""

███╗░░░███╗██╗██╗░░██╗██╗░░░██╗░░░░░░██████╗░░█████╗░████████╗
████╗░████║██║██║░██╔╝██║░░░██║░░░░░░██╔══██╗██╔══██╗╚══██╔══╝
██╔████╔██║██║█████═╝░██║░░░██║█████╗██████╦╝██║░░██║░░░██║░░░
██║╚██╔╝██║██║██╔═██╗░██║░░░██║╚════╝██╔══██╗██║░░██║░░░██║░░░
██║░╚═╝░██║██║██║░╚██╗╚██████╔╝░░░░░░██████╦╝╚█████╔╝░░░██║░░░
╚═╝░░░░░╚═╝╚═╝╚═╝░░╚═╝░╚═════╝░░░░░░░╚═════╝░░╚════╝░░░░╚═╝░░░
""")

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
    global STDOUT_CHANNEL
    STDOUT_CHANNEL = await client.fetch_channel(885979416369438751)
    await STDOUT_CHANNEL.send(f"Miku {__version__} Online.")

@client.event
async def on_guild_join(guild):
    logger.info(f"Joined guild {guild.name}")
    await STDOUT_CHANNEL.send(f"Joined guild `{guild.name}`\nTotal Guilds: {len(client.guilds)}")
    open("utils/guilds.txt", "a").write(f"\n{guild.id}")
    await client.close()
    os.system("python3 main.py")

@client.command()
async def reload(ctx, module):
    try:
        client.reload_extension(f"cogs.{module}")
        logger.info(f"Reloaded extension {module}")
        await ctx.send(f"Reloaded extension {module}")
    except Exception as e:
        logger.error(f"Failed to reload extension: {e}")
        await ctx.send(f"Failed to reload extension: {e}")


@client.event
async def on_guild_remove(guild):
    logger.info(f"Left guild {guild.name}")
    await STDOUT_CHANNEL.send(f"Left guild `{guild.name}`\nTotal Guilds: {len(client.guilds)}")
    with open("utils/guilds.txt", "r") as f:
        lines = f.readlines()
    with open("utils/guilds.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != str(guild.id):
                f.write(line)


@client.event
async def on_disconnect():
    logger.info("Disconnected from Discord")
    await STDOUT_CHANNEL.send(f"Disconnected from Discord")

@client.event
async def on_connect():
    logger.info("Connected to Discord")
    logger.info(
        f"Logged in as {client.user.name}#{client.user.discriminator}")

#owner only commands
@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down...")
    await client.close()

@client.command()
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    """Function to change bot prefix from the default

    Args:
        prefixes (str, optional): Prefix to be used. Defaults to "".
    """
    custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes
    await ctx.send("Prefixes set!")


MAIN_HELP = "**Miku** - The only music bot you'll ever need!\nDiscord will only be supporting slash commands soon. Use `/help` for commands."

MUSIC_HELP = """
**`join`**: 
    Connect the bot your current Voice Channel.

**`play <song_name | url>`**: 
    Play a song from YouTube given a search term or URL.

**`stop`**: 
    Stop playing the song.

**`pause`**: 
    Pause the song currently playing.

**`resume`**: 
    Resume playing the song.

**`skip`**:
    Skip the current song.

**`leave`**:
    Leave the vc.

**`queue`**:
    Display the current queue.

"""

OTHER_HELP = """
**`botinfo`**: 
    Some info about the Bot.
**`setprefix`**:
    Set a custom prefix for the Bot.
**`avatar`**:
    Get your own/another user's avatar.
"""


# help command
@client.command(name="help", description="List commands")
async def command_help(ctx):
    "Main help command for the bot"
    bot_help = discord.Embed(
        title="Miku Help",
        description=MAIN_HELP,
        color=discord.Color.from_rgb(3, 252, 252))
    bot_help.set_thumbnail(url=client.user.avatar_url)
    await ctx.send(embed=bot_help)


@slash.slash(name="help", guild_ids=__GUILD_ID__, description="list all commands.")
async def _help(ctx):
    select = create_select(
        options=[  # the options in your dropdown
            create_select_option("Music", value="m00sik", emoji="🎶"),
            create_select_option("Other", value="settings", emoji="⚙️"),
        ],
        # the placeholder text to show when no options have been chosen
        placeholder="Select Category",
        min_values=1,  # the minimum number of options a user must select
        max_values=1,  # the maximum number of options a user can select
    )

    action_row = create_actionrow(select)
    bot_help = discord.Embed(
        title="Miku Help",
        description=f"Select Category for commands.",
        color=discord.Color.from_rgb(3, 252, 252))
    await ctx.send(embed=bot_help, components=[action_row])


@client.event
async def on_component(ctx: ComponentContext):
    # ctx.selected_options is a list of all the values the user selected
    music = discord.Embed(
        title="Music Commands",
        description=MUSIC_HELP,
        color=discord.Color.from_rgb(3, 252, 252)
    )
    sets = discord.Embed(
        title="Other Commands",
        description=OTHER_HELP,
        color=discord.Color.from_rgb(3, 252, 252)
    )

    if 'm00sik' in ctx.selected_options:
        await ctx.edit_origin(embed=music)
    elif 'settings' in ctx.selected_options:
        await ctx.edit_origin(embed=sets)


command_modules = [
    module[:-3]
    for module in os.listdir(f"{os.path.dirname(__file__)}/cogs")
    if module[-3:] == ".py"
]

if command_modules:
    logger.info("Importing cogs. Please stand by...")
    logger.info(
        f"Importing {len(command_modules)} cogs: {', '.join(command_modules)}")
else:
    logger.info("Could not import any cogs!")

# dynamically load all cogs found in cogs/ as cog extensions
for module in command_modules:
    try:
        client.load_extension("cogs." + module)
    except Exception as e:
        logger.info(f"Could not import cog {module}: \n{e}")

logger.info(f"Cogs imported: {', '.join(command_modules)}")

client.run(TOKEN)