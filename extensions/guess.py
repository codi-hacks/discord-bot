import discord
from discord.ext import commands
import random
from main import get_prefix

# Name of the command that activates the game.
COMMAND = 'guess'
# Prefix registeration
PREFIX = get_prefix()

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

    @commands.command(name=COMMAND)
    async def guess(self, ctx):
        """Guess the number"""
        self.guesser = ctx.author
        self.active = True
        await ctx.send('''Starting guessing game with <@!{}>
Guess a number between 1 and 100. Stop guessing to quit.'''.format(ctx.author.id))

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.guesser and self.active == True and COMMAND not in ctx.content:
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
