"""
Meta commands for the Miku bot
"""

import asyncio
import datetime
import time
from typing import Text
from faker import Faker
from faker.providers import internet, user_agent
import discord
from discord.enums import ChannelType
from discord.ext import commands
from discord.ext.commands.core import guild_only
from discord_slash import SlashCommand, SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import (create_actionrow,
                                                   create_select,
                                                   create_select_option)

from utils import logutil
from random import choice
cards = ['visa', 'mastercard', 'discover', 'amex', 'jcb', 'diners', 'visa16']
__GUILD_ID__ = []
for i in open("./utils/guilds.txt", "r").read().split("\n"):
    if i:
        __GUILD_ID__.append(int(i.replace("'", "")))

logger = logutil.init()
fake = Faker()
fake.add_provider(internet)
fake.add_provider(user_agent)

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

    @cog_ext.cog_slash(name="botinfo", description="Display info about the bot", guild_ids=__GUILD_ID__)
    async def command_botinfo(self, ctx: SlashContext):
        "Returns information about the bot"

        logger.info(f"{ctx.author} executed botinfo")

        SKYASCII = ctx.guild.get_member(614053918867062785)
        ADIL = ctx.guild.get_member(613789929134227465)
        MARSH = ctx.guild.get_member(614058101347188737)

        user = ctx.guild.get_member(886914091657101313)
        info = discord.Embed(
            title="Bot Info",
            color=discord.Color.from_rgb(3, 252, 252)
        )
        info.set_author(
            name=f"{user.display_name}#{user.discriminator}", icon_url=user.avatar_url)
        info.add_field(name="ID", value=self.client.user.id, inline=True)
        info.add_field(name="Created on",
                       value=user.created_at.strftime("%a, %b %d, %Y %I:%M %p"))
        #info.add_field(name="Joined on", value=member.joined_at.strftime("%a, %b %d, %Y %I:%M %p"))
        uptime = str(datetime.timedelta(
            seconds=int(round(time.time()-startTime))))
        info.add_field(name="Library used",
                       value="Enhanced Discord.py v1.7.3.7.post1", inline=False)
        info.add_field(name="Python Version",
                       value="Python 3.9.6", inline=True)
        info.add_field(name="Code Lines written", value="492")
        info.add_field(name="Uptime", value=uptime, inline=False)
        info.add_field(name="Top Role in this Server", value=user.top_role)
        info.add_field(
            name="Dev Team", value="Adil#5514 ,Skyascii#1860, marshadow#7063", inline=False)
        info.add_field(name="Version", value='1.3.0')
        info.set_footer(text="Avatar drawn by marshadow#7063")
        info.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=info)

    @cog_ext.cog_slash(name="serverinfo", description="Get server info", guild_ids=__GUILD_ID__)
    async def command_serverinfo(self, ctx: SlashContext):

        info = discord.Embed(
            color=discord.Color.from_rgb(3, 252, 252)
        )
        info.set_author(
            name=f"{ctx.guild.name}", icon_url=ctx.guild.icon_url)
        info.add_field(
            name="Owner", value=f"{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}", inline=True)
        info.add_field(name="Channel Categories",
                       value=len(ctx.guild.categories))
        info.add_field(name="Text Channels",
                       value=len(ctx.guild.text_channels), inline=True)
        info.add_field(name="Voice Channels",
                       value=len(ctx.guild.voice_channels))
        info.add_field(name="Members", value=len(
            [m for m in ctx.guild.members if not m.bot]))
        info.add_field(name="Bots", value=len(
            [m for m in ctx.guild.members if not m.bot]))
        info.add_field(name="Roles", value=len(ctx.guild.roles))
        info.add_field(name="Role list", value=", ".join(
            [str(r.name) for r in ctx.guild.roles]), inline=False)
        info.set_thumbnail(url=ctx.guild.icon_url)
        info.set_footer(
            text=f'ID: {ctx.guild.id} | Created on {ctx.guild.created_at.strftime("%a, %b %d, %Y %I:%M %p")}')
        await ctx.send(embed=info)

    # get user's avatar
    @cog_ext.cog_slash(name="avatar", description="Get user's avatar", guild_ids=__GUILD_ID__,
                       options=[
                           create_option(
                               name="user",
                               description="Select user to get avatar",
                               option_type=6,
                               required=False)
                       ])
    async def command_avatar(self, ctx: SlashContext, user=None):
        "Returns the avatar of the user"
        if user:
            pass
        else:
            user = ctx.author
        info = discord.Embed(
            title=f"{user.display_name}'s Avatar",
            color=discord.Color.from_rgb(3, 252, 252)
        )
        info.set_author(
            name=f"{user.display_name}#{user.discriminator}", icon_url=user.avatar_url)
        info.set_image(url=user.avatar_url)
        info.set_footer(text=f'ID: {user.id}')
        await ctx.send(embed=info)

    @cog_ext.cog_slash(name="hack", description="Very real hacking", guild_ids=__GUILD_ID__,
    options=[
        create_option(
            name="user",
            description="Select user to hack",
            option_type=6,
            required=True)
    ])
    async def command_hack(self, ctx: SlashContext, user: discord.Member):
        msg = await ctx.send(f"Initiating hack on {user.display_name}. Please wait...")
        await asyncio.sleep(1)
        await msg.edit(content="Getting user's IP address")
        await asyncio.sleep(0.25)
        await msg.edit(content=f"{fake.ipv4_private()}")
        await asyncio.sleep(0.5)
        await msg.edit(content="Getting user's email id and discord password")
        await asyncio.sleep(0.25)
        await msg.edit(content=f"Email: {fake.free_email}\nPassword: {fake.password()}")
        await asyncio.sleep(0.5)
        await msg.edit(content="Locating user")
        await asyncio.sleep(0.25)
        await msg.edit(content=f"{fake.address()}")
        await asyncio.sleep(0.5)
        await msg.edit(content="Grabbing user's phone number")
        await asyncio.sleep(0.25)
        await msg.edit(content=f"{fake.phone_number()}")
        await asyncio.sleep(0.5)
        await msg.edit(content="Logging user's User Agent")
        await asyncio.sleep(0.25)
        await msg.edit(content=f"{fake.user_agent()}")
        await asyncio.sleep(0.5)
        await msg.edit(content="Stealing credit card information")
        await asyncio.sleep(0.25)
        await msg.edit(content=f"{fake.credit_card_full(card_type=choice(cards))}")
        await asyncio.sleep(0.5)
        await msg.edit(content="Hacking Steam account")
        await asyncio.sleep(0.25)
        await msg.edit(content=f"{fake.user_name()}")
        await asyncio.sleep(0.5)
        await msg.edit(content="Hack Completed")
        em = discord.Embed(
            title="Hacked Information",
            description=f"**IP Address**: {fake.ipv4_private()}\n**Email**: {fake.email(domain='gmail.com')}\n**Password**: {fake.password()}\n**Address**: {fake.address()}\n**Phone Number**: {fake.phone_number()}\n**User Agent**: {fake.user_agent()}\n**Credit Card Info**: {fake.credit_card_full(card_type=choice(cards))}",
            color=discord.Color.from_rgb(3, 252, 252)
        )
        em.set_thumbnail(url=user.avatar_url)
        em.set_footer(text="source: trust me bro")
        await msg.edit(embed=em)


    async def _ping(self, ctx: SlashContext):
        "Returns the latency of the bot"
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")
        
    @cog_ext.cog_slash(name="ping", description="Pong!", guild_ids=__GUILD_ID__)
    async def _slash_ping(self, ctx: SlashContext):
        await self._ping(ctx)

    @commands.command(name="ping", aliases=["pong"],)
    async def _reg_ping(self, ctx):
        await self._ping(ctx)

    @commands.Cog.listener()
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"Error: {error.original}")
        elif isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Error: Missing required argument {error.param}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Error: Bad argument {error.param}")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f"Error: {error.__class__.__name__}")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Error: {error.retry_after}")
        elif isinstance(error, commands.CommandError):
            await ctx.send(f"Error: {error.__class__.__name__}")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"Error: Missing permissions {error.missing_perms}")
        else:
            await ctx.send(f"Error: {error}")

def setup(bot):
    "Setup command for the bot"

    bot.add_cog(Meta(bot))
