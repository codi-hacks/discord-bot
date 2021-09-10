import discord
from discord.ext import commands
import yaml

with open('config.yml', 'r') as file:
  config = yaml.safe_load(file)

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Prefixes may also contain spaces
    prefixes = ['.']

    return commands.when_mentioned_or(*prefixes)(bot, message)

#bot = discord.Client()
bot = commands.Bot(command_prefix='.', description='CodiHacks bot')

# Load cogs by the filenames
bot.load_extension('guess')
bot.load_extension('rng')

# Event listeners
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$halo'):
        await message.channel.send('Hello!')

# Initialize bot
bot.run(config['discord_token'], bot=True, reconnect=True)
