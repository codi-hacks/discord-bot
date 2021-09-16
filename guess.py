import discord
from discord.ext import commands
import random

class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # The number the user is trying to guess
        self.number = self.generate_number()
        # Number of guesses made at getting the right number
        self.attempts = 0

    def generate_number(self):
        return random.randint(0, 100)

    @commands.command(name='guess')
    async def guess(self, ctx):
        """Guess the number"""
        try:
            guessed_number = int(ctx.message.clean_content.split(' ')[-1])
        except Exception:
            await ctx.send('Guess a number between 0 and 100')
            return

        self.attempts += 1

        if guessed_number > self.number:
            await ctx.send('Too high.')
            return

        if guessed_number < self.number:
            await ctx.send('Too low.')
            return

        await ctx.send(
            '{0}. You guessed right! Guesses made: {1}'.format(
                self.number,
                self.attempts
            )
        )
        self.number = self.generate_number()
        self.attempts = 0

def setup(bot):
    bot.add_cog(Guess(bot))
