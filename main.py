import discord
from discord.ext import commands
import yaml
import os

with open('config.yml', 'r') as file:
  config = yaml.safe_load(file)

def get_prefix():
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Prefixes may also contain spaces
    prefixes = ['.']

    return commands.when_mentioned_or(*prefixes)

#bot = discord.Client()
bot = commands.Bot(command_prefix=get_prefix(), description='CodiHacks bot')

# Load cogs by the filenames
for i in os.listdir('extensions'):
	if i.endswith('.py') and os.path.isfile('extensions/' + i):
		bot.load_extension('extensions.' + i.replace('.py', ''))

# Event listeners
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# Initialize bot
bot.run(config['discord_token'], bot=True, reconnect=True)
