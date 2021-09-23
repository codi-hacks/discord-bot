import discord
from discord.ext import commands
import random
from main import get_prefix

# Name of the command that activates the game.
COMMAND = 'hangman'
# Prefix registeration
PREFIX = get_prefix()



class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # The number the user is trying to guess
        self.word = self.generate_word()
        # Number of guesses made at getting the right number
        self.attempts = 0
        # Track who is actually playing the game.
        self.guesser = ''
        # Track if the game is active.
        self.active = False

    def generate_word(self):
        with open ("extensions\\words_for_hangman.txt",'r') as f:
            for i in f.readlines():
                word_list = i.split('|')
        index = random.randint(0,len(word_list)-1)
        return word_list[index]

    @commands.command(name=COMMAND)
    async def guess(self, ctx):
        """Guess the number"""
        self.guesser = ctx.author
        self.active = True
        await ctx.send('''Starting guessing game with <@!{}>
Start guessing letters and see if you can solve for the word. Stop guessing to quit.'''.format(ctx.author.id))

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

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.guesser and self.active == True and COMMAND not in ctx.content:
            await ctx.channel.send(
                '_'*len(self.word)
            )

def setup(bot):
    bot.add_cog(Hangman(bot))