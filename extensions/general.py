import discord
from discord.ext import commands
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Get the current bot version', aliases=['ver', 'about', 'info'])
    async def version(self, ctx):
        await ctx.send("DarK`BoT by Codi-Hacks")

def setup(bot):
    bot.add_cog(General(bot))
