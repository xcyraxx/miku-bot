from os import name, terminal_size
import discord
import datetime, time
from discord import member 
from main import __version__

from discord.ext import commands
from discord.ext.commands.core import command

#this is very important for creating a cog
class Meta(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Meta up!') 
        global startTime 
        startTime = time.time()

    #create a command in the cog
    @commands.command(name='Uptime')
    async def _uptime(self,ctx):

        # what this is doing is creating a variable called 'uptime' and assigning it
        # a string value based off calling a time.time() snapshot now, and subtracting
        # the global from earlier
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        await ctx.send(uptime)

    @commands.command(name="botinfo", aliases=("bi", ))
    async def command_botinfo(self, ctx):
        "Returns information about the bot"
        user = ctx.guild.get_member(886914091657101313)
        perm_list = [perm[0] for perm in user.guild_permissions if perm[1]]
        info = discord.Embed(
            title="Bot Info",
            color=discord.Color.from_rgb(3, 252, 252)
        )
        info.set_author(name=f"{user.display_name}#{user.discriminator}", icon_url=user.avatar_url)
        info.add_field(name="ID", value=self.client.user.id, inline=True)
        info.add_field(name="Created on",
                    value=user.created_at.strftime("%a, %b %d, %Y %I:%M %p"))
        #info.add_field(name="Joined on", value=member.joined_at.strftime("%a, %b %d, %Y %I:%M %p"))
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        info.add_field(name="Library used", value="Enhanced Discord.py v1.7.3.7.post1", inline=False)
        info.add_field(name="Python Version", value="Python 3.9.6", inline=True)
        info.add_field(name="Code Lines written", value="394")
        info.add_field(name="Uptime", value=uptime, inline=False)
        info.add_field(name="Top Role in this Server" ,value=user.top_role)
        info.add_field(name="Team? ig?", value="Adil#5514 Skyascii#1860 marshadow#7063", inline=False)
        info.add_field(name="Version", value=f"{__version__}")
        info.set_footer(text="Avatar drawn by marshadow#7063")
        info.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=info)

def setup(bot):
    bot.add_cog(Meta(bot))  