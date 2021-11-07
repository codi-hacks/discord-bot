import discord
import subprocess
from discord.ext import commands
import random

# Basic commands a bot should have:

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Version command, takes the Revision from last commit and shows it as the revision #
    @commands.command(description='Get the current bot version', aliases=['ver', 'version', 'info'])
    async def about(self, ctx):
        try:
            ver = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()
            await ctx.send("DarK`BoT by Codi-Hacks rev: " + ver)
        except Exception:
            await ctx.send("DarK`BoT by Codi-Hacks")

    #Say command, it echoes whatever you tell it
    @commands.command()
    async def say(self, ctx):
        message = ctx.message.clean_content
        final = message.split(' ', 1)[1]
        try:
            await ctx.send(final)
        except:
            await ctx.send("Please Give Some Message!")

def setup(bot):
    bot.add_cog(General(bot))