"""
Master script for Miku

Main contributors:
    @savioxavier, @xcyraxx, @UnderdriveAssassin
"""
# ol(

import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils import logutil

load_dotenv()

TOKEN = os.environ.get("TOKEN")

__version__ = "2.0"
__GUILD_ID__ = [846609621429780520, 893122121805496371]


intents = discord.Intents.default()
intents.members = True

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
client = commands.Bot(command_prefix=">>",
                      case_insensitive=True,
                      activity=activity,
                      intents=intents,
                      help_command=None,
                      status=discord.enums.Status.idle
                      )


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
music = discord.Embed(
    title="Miku Music Help",
    description=MUSIC_HELP,
    color=discord.Color.from_rgb(3, 252, 252))

OTHER_HELP = """
**`botinfo`**: 
    Some info about the Bot.
**`setprefix`**:
    Set a custom prefix for the Bot.
**`avatar`**:
    Get your own/another user's avatar.
"""
other = discord.Embed(
    title="Miku Other Help",
    description=OTHER_HELP,
    color=discord.Color.from_rgb(3, 252, 252))


class DropDown(discord.ui.View):
    @discord.ui.select(
        placeholder="Select a category",
        options=[
            discord.SelectOption(label="Music", value="music", emoji="🎵"),
            discord.SelectOption(label="Other", value="other", emoji="🔧"),
        ]
    )
    async def callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "music":
            await interaction.response.edit_message(embed=music)
        elif select.values[0] == "other":
            await interaction.response.edit_message(embed=other)
        else:
            await interaction.response.send_message("Invalid category")
# help command


@client.command(name="help", description="List commands")
async def _reg_help(ctx):
    await _help(ctx)


@client.command(name="test", description="Test command")
async def _reg_test(ctx):
    msg = await ctx.send("Test command")
    await asyncio.sleep(5)
    await msg.edit(content="Test command edited")


@client.slash_command(name="help", guild_ids=__GUILD_ID__, description="list all commands.")
async def _slash_help(ctx):
    await _help(ctx)


async def _help(ctx):
    view = DropDown()
    bot_help = discord.Embed(
        title="Miku Help",
        description="Select Category for commands.",
        color=discord.Color.from_rgb(3, 252, 252))
    await ctx.respond(embed=bot_help, view=view)
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


@client.slash_command(name="activity", guild_ids=__GUILD_ID__, description="Set the bot's activity")
@commands.is_owner()
async def _slash_activity(ctx, *, activity=None):
    await client.change_presence(activity=discord.Game(name=activity), status=discord.enums.Status.idle)
    await ctx.respond(f"Activity set to {activity}")

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
