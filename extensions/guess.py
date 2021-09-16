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
        # Track who is actually playing the game.
        self.guesser = ''
        # Track if the game is active.
        self.active = False

    def generate_number(self):
        return random.randint(0, 100)

    @commands.command(name='guess')
    async def guess(self, ctx):
        """Guess the number"""
        self.guesser = ctx.author
        self.active = True
        await ctx.send('Starting guessing game with {}'.format(ctx.author))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.guesser and self.active == True and ctx.content.split(' ')[0] != '.guess':
            try:
                guessed_number = int(ctx.content)
            except ValueError:
                await ctx.channel.send('Quitting guessing game...')
                self.number = self.generate_number()
                self.attempts = 0
                self.active = False
                return

            self.attempts += 1

            if guessed_number > self.number:
                await ctx.channel.send('Too high.')
                return

            if guessed_number < self.number:
                await ctx.channel.send('Too low.')
                return

            await ctx.channel.send(
                '{0}. You guessed right! Guesses made: {1}'.format(
                    self.number,
                    self.attempts
                )
            )
            self.number = self.generate_number()
            self.attempts = 0
            self.active = False
        return

def setup(bot):
    bot.add_cog(Guess(bot))
