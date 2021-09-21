"""
Meta commands for the Miku bot
"""

import datetime
import time
import discord
from discord.ext import commands


# this is very important for creating a cog
class Meta(commands.Cog):
    "Python class that handles all meta commands"

    def __init__(self, client):
        "Init function for Discord client"

        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        "Function to determine what commands are to be if bot is connected to Discord"

        print("Meta up!")
        global startTime
        startTime = time.time()

    # create a command in the cog
    @commands.command(name="Uptime")
    async def _uptime(self, ctx):

        # what this is doing is creating a variable called "uptime" and assigning it
        # a string value based off calling a time.time() snapshot now, and subtracting
        # the global from earlier
        uptime = str(datetime.timedelta(
            seconds=int(round(time.time()-startTime))))
        await ctx.send(uptime)

    @commands.command(name="botinfo", aliases=("bi", ))
    async def command_botinfo(self, ctx):
        "Returns information about the bot"

        SKYASCII = ctx.guild.get_member(614053918867062785)
        ADIL = ctx.guild.get_member(613789929134227465)
        MARSH = ctx.guild.get_member(614058101347188737)

        skyascii = f"{SKYASCII.name}#{SKYASCII.discriminator}"
        adil = f"{ADIL.name}#{ADIL.discriminator}"
        marsh = f"{MARSH.name}#{MARSH.discriminator}"


        user = ctx.guild.get_member(886914091657101313)
        perm_list = [perm[0] for perm in user.guild_permissions if perm[1]]
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
            name="Dev Team", value=f"{skyascii}, {adil}, {marsh}", inline=False)
        info.add_field(name="Version", value='1.2.0')
        info.set_footer(text="Avatar drawn by marshadow#7063")
        info.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=info)


def setup(bot):
    "Setup command for the bot"

    bot.add_cog(Meta(bot))
