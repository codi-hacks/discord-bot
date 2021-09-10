import discord
from discord.ext import commands

class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.number = None

    @commands.command(name='guess')
    async def guess(self, ctx, *, member: discord.Member = None):
        """Guess the number"""
        if not self.number:
            self.number = random.randint(0, 100)

        ctx.send('Number is {0}'.format(self.number))

# We give bot.add_cog() the class name defined above
def setup(bot):
    bot.add_cog(Guess(bot))
