"""
Master script for Miku

Main contributors:
    @savioxavier, @xcyraxx, @UnderdriveAssassin
"""
# ol(

import os
from gc import set_threshold

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_components import (ComponentContext,
                                                   create_actionrow,
                                                   create_select,
                                                   create_select_option,
                                                   wait_for_component)
from dotenv import load_dotenv

from utils import logutil

load_dotenv()

TOKEN = os.environ.get("TOKEN")

__version__ = "2.0"
__GUILD_ID__ = [846609621429780520, 893122121805496371]

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

activity = discord.Game(name=">>help • /help")
client = commands.Bot(command_prefix=determine_prefix,
                      case_insensitive=True,
                      activity=activity,
                      intents=intents,
                      help_command=None,
                      status=discord.enums.Status.idle
                      )
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    "Function to determine what commands are to be if bot is connected to Discord"
    logger.info(
        f"Logged in as {client.user.name}#{client.user.discriminator}")
    STDOUT_CHANNEL = await client.fetch_channel(885979416369438751)
    await STDOUT_CHANNEL.send(f"Miku {__version__} Online.")

@client.event
async def on_disconnect():
    STDOUT_CHANNEL = await client.fetch_channel(885979416369438751)
    await STDOUT_CHANNEL.send(f"Miku {__version__} Offline.")

@client.command()
@commands.guild_only()
async def setprefix(ctx, *, prefixes=""):
    """Function to change bot prefix from the default

    Args:
        prefixes (str, optional): Prefix to be used. Defaults to "".
    """
    custom_prefixes[ctx.guild.id] = prefixes.split() or default_prefixes
    await ctx.send("Prefixes set!")

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

**`remove`**:
    Remove a song from the queue.

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
async def _reg_help(ctx):
    await _help(ctx)


@slash.slash(name="help", guild_ids=__GUILD_ID__, description="list all commands.")
async def _slash_help(ctx):
    await _help(ctx)


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
        description="Select Category for commands.",
        color=discord.Color.from_rgb(3, 252, 252))
    await ctx.send(embed=bot_help, components=[action_row])
    logger.info(f"{ctx.author} requested help.")

@client.command(name="activity", description="Set the bot's activity")
@commands.is_owner()
async def _reg_activity(ctx, *, activity=None):
    await client.change_presence(activity=discord.Game(name=activity), status=discord.enums.Status.idle)
    await ctx.send(f"Activity set to {activity}")

@_reg_activity.error
async def _reg_activity_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the required permissions.")

@client.event
async def on_component(ctx: ComponentContext):
    # ctx.selected_options is a list of all the values the user selected
    music = discord.Embed(
        title="Miku Help",
        description=MUSIC_HELP,
        color=discord.Color.from_rgb(3, 252, 252)
    )
    sets = discord.Embed(
        title="Miku Help",
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
