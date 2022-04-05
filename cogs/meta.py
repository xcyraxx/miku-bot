"""
Meta commands for the Miku bot
"""

import datetime
import time

import discord
from discord.ext import commands

from utils import logutil

__GUILD_ID__ = [846609621429780520, 893122121805496371]

logger = logutil.init()


def get_all_roles(user):
    "Get all roles for a user"

    return ",".join(
        [f"<@&{role.id}>" for role in user.roles if role.name != "@everyone"]
    )


"""
TOO MANY PERMS X
def get_all_perms(user):
    perms = []
    role = user.top_role
    for name, value in role.permissions:
        if value:
            perms.append(name)
    return perms
"""


def get_key_perms(user):
    "Get the key permissions for a user"

    role = user.top_role
    key_perms = [
        "administrator",
        "manage_guild",
        "manage_channels",
        "kick members",
        "ban members",
        "manage_nicknames",
        "manage_roles",
        "manage_messages",
        "attach files",
        "mention everyone",
        "manage_webhooks",
        "manage_emojis",
    ]

    return [name for name, value in role.permissions if value and name in key_perms]


class Meta(commands.Cog):
    "Python class that handles all meta commands"

    def __init__(self, client):
        "Init function for Discord client"

        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        "Function to determine what commands are to be if bot is connected to Discord"

        logger.info("Meta up!")
        global startTime
        startTime = time.time()

    @discord.slash_command(
        name="botinfo", description="Display info about the bot", guild_ids=__GUILD_ID__
    )
    async def command_botinfo(self, ctx):
        "Returns information about the bot"

        logger.info(f"{ctx.author} executed botinfo")

        SKYASCII = ctx.guild.get_member(614053918867062785)
        ADIL = ctx.guild.get_member(613789929134227465)
        MARSH = ctx.guild.get_member(614058101347188737)

        user = ctx.guild.get_member(886914091657101313)
        info = discord.Embed(
            title="Bot Info", color=discord.Color.from_rgb(3, 252, 252)
        )
        info.set_author(
            name=f"{user.display_name}#{user.discriminator}", icon_url=user.avatar_url
        )
        info.add_field(name="ID", value=self.client.user.id, inline=True)
        info.add_field(
            name="Created on", value=user.created_at.strftime("%a, %b %d, %Y %I:%M %p")
        )
        # info.add_field(name="Joined on", value=member.joined_at.strftime("%a, %b %d, %Y %I:%M %p"))
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - startTime))))
        info.add_field(name="Library used", value="Py-cord", inline=False)
        info.add_field(name="Python Version", value="Python 3.9.6", inline=True)
        info.add_field(name="Code Lines written", value="913")
        info.add_field(name="Uptime", value=uptime, inline=False)
        info.add_field(name="Top Role in this Server", value=user.top_role)
        info.add_field(
            name="Dev Team",
            value="Adil#5514 ,Skyascii#1860, marshadow#7063",
            inline=False,
        )
        info.add_field(name="Version", value="1.3.0")
        info.set_footer(text="Avatar drawn by marshadow#7063")
        info.set_thumbnail(url=user.avatar_url)
        await ctx.respond(embed=info)

    @discord.slash_command(
        name="serverinfo", description="Get server info", guild_ids=__GUILD_ID__
    )
    async def command_serverinfo(self, ctx):

        info = discord.Embed(color=discord.Color.from_rgb(3, 252, 252))
        info.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)
        info.add_field(
            name="Owner",
            value=f"{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}",
            inline=True,
        )
        info.add_field(name="Channel Categories", value=len(ctx.guild.categories))
        info.add_field(
            name="Text Channels", value=len(ctx.guild.text_channels), inline=True
        )
        info.add_field(name="Voice Channels", value=len(ctx.guild.voice_channels))
        info.add_field(
            name="Members", value=len([m for m in ctx.guild.members if not m.bot])
        )
        info.add_field(
            name="Bots", value=len([m for m in ctx.guild.members if not m.bot])
        )
        info.add_field(name="Roles", value=len(ctx.guild.roles))
        info.set_thumbnail(url=ctx.guild.icon.url)
        info.set_footer(
            text=f'ID: {ctx.guild.id} | Created on {ctx.guild.created_at.strftime("%a, %b %d, %Y %I:%M %p")}'
        )
        await ctx.respond(embed=info)

    # get user's avatar
    @discord.slash_command(
        name="avatar", description="Get user's avatar", guild_ids=__GUILD_ID__
    )
    async def command_avatar(self, ctx, user: discord.User = None):
        "Returns the avatar of the user"
        if not user:
            user = ctx.author
        info = discord.Embed(
            title=f"{user.display_name}'s Avatar",
            color=discord.Color.from_rgb(3, 252, 252),
        )
        info.set_author(
            name=f"{user.display_name}#{user.discriminator}", icon_url=user.avatar.url
        )
        info.set_image(url=user.avatar.url)
        info.set_footer(text=f"ID: {user.id}")
        await ctx.respond(embed=info)

    @discord.slash_command(
        name="whois", description="Get user's info", guild_ids=__GUILD_ID__
    )
    async def command_whois(self, ctx, user: discord.User = None):
        "Returns the info of the user"
        if not user:
            try:
                user = ctx.author
            except AttributeError:
                user = ctx.author
        info = discord.Embed(
            title=f"{user.display_name}'s Info",
            color=discord.Color.from_rgb(3, 252, 252),
        )
        info.set_author(
            name=f"{user.display_name}#{user.discriminator}", icon_url=user.avatar.url
        )
        info.add_field(
            name="Register on",
            value=user.created_at.strftime("%a, %b %d, %Y %I:%M %p"),
            inline=True,
        )
        info.add_field(
            name="Joined on",
            value=user.joined_at.strftime("%a, %b %d, %Y %I:%M %p"),
            inline=True,
        )
        info.add_field(
            name=f"Roles[{len(user.roles)-1}]", value=get_all_roles(user), inline=False
        )
        info.add_field(
            name="Key Permissions",
            value=",".join(
                f"{perm.capitalize().replace('_', ' ')}" for perm in get_key_perms(user)
            ),
            inline=False,
        )
        info.set_footer(text=f"ID: {user.id}")
        info.set_thumbnail(url=user.avatar.url)
        await ctx.respond(embed=info)

    @command_whois.error
    async def command_whois_error(self, ctx, error):
        logger.error(error)


def setup(bot):
    "Setup command for the bot"

    bot.add_cog(Meta(bot))
