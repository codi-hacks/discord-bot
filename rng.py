from discord.ext import commands
import random

class RNG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx):
        """Rolls a dice in NdN format."""
        #
        # Sanity checks yay!
        #
        try:
            rolls, limit = map(int, ctx.message.content.split(' ')[-1].split('d'))
        except Exception:
            await ctx.send('Format has to be in NdN!')
            return

        if rolls < 1 or rolls > 100:
            await ctx.send("That's an unreasonable number of dice")
            return

        if limit < 1:
            await ctx.send("A die with that many sides breaks the fundamental laws of physics.")
            return

        if limit > 1000000:
            await ctx.send('Ok a die with that many sides is clearly just a sphere.')
            return

        #
        # Actual code
        #
        results = list(map(lambda x: random.randint(1, limit), range(rolls)))

        if len(results) == 1:
            await ctx.send(str(results[0]))
            return

        total = sum(results)
        results = ' + '.join(map(str, results))
        await ctx.send('{0} = {1}'.format(results, total))

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx):
        """Chooses between multiple choices."""
        [*choices] = ctx.message.clean_content.split(', ')

        if len(choices) < 2:
            await ctx.send("Tell me some choices you have, separated by commas. I'll choose one for you.")
            return

        await ctx.send(random.choice(choices))

def setup(bot):
    bot.add_cog(RNG(bot))
