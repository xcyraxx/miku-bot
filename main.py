"""
Master script for Miku

Main contributors:
    @savioxavier, @xcyraxx, @UndriveAssassin
    Assassin
"""
#ol(

from gc import set_threshold
import os
import discord
from discord.enums import Status
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
from discord_slash import SlashCommand
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import wait_for_component, ComponentContext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow


load_dotenv()
TOKEN = os.environ.get("TOKEN")

__version__ = "1.3.0"
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

print("""

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
    "Function to determine what commands are to be if bot is connected to Discord"
    print(f"logged in as {client.user.name}#{client.user.discriminator}")
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


MAIN_HELP = "**Miku** - The only music bot you'll ever need!\nDiscord will only be supporting slash commands soon. Use `/help` for commands."

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
**`setprefix`**:
    Set a custom prefix for the Bot.
"""


#help command
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
        options=[# the options in your dropdown
            create_select_option("Music", value="m00sik", emoji="🎶"),
            create_select_option("Other", value="settings", emoji="⚙️"),
        ],
        placeholder="Select Category",  # the placeholder text to show when no options have been chosen
        min_values=1,  # the minimum number of options a user must select
        max_values=1,  # the maximum number of options a user can select
    )

    action_row = create_actionrow(select)
    bot_help = discord.Embed(
        title="Miku Help",
        description="Select Category for commands.",
        color=discord.Color.from_rgb(3, 252, 252))
    await ctx.send(embed = bot_help, components = [action_row])

@client.event
async def on_component(ctx: ComponentContext):
    # ctx.selected_options is a list of all the values the user selected
    music = discord.Embed(
        title = "Miku Help",
        description = MUSIC_HELP,
        color=discord.Color.from_rgb(3, 252, 252)
    )
    sets = discord.Embed(
        title = "Miku Help",
        description = OTHER_HELP,
        color=discord.Color.from_rgb(3, 252, 252)
    )
    
    if 'm00sik' in ctx.selected_options:
        await ctx.edit_origin(embed = music)
        pass
    elif 'settings' in ctx.selected_options:
        await ctx.edit_origin(embed = sets)
        pass


client.load_extension("cogs.music")
client.load_extension("cogs.meta")
client.run(TOKEN)
