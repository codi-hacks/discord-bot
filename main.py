import discord
from discord.ext import commands
import os
import yaml

with open('config.yml', 'r') as file:
  config = yaml.safe_load(file)

def get_prefix():
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    prefixes = config['command_prefixes']
    if not isinstance(prefixes, list):
        raise ValueError('Config file does not prefix "command_prefixes" list. See config.yml.example.')

    return commands.when_mentioned_or(*prefixes)

#bot = discord.Client()
bot = commands.Bot(command_prefix=get_prefix(), description='CodiHacks bot')

# Load cogs by the filenames
extensionCounter = 0
for i in os.listdir('extensions'):
    if i.endswith('.py') and os.path.isfile('extensions/' + i):
        bot.load_extension('extensions.' + i.replace('.py', ''))
        extensionCounter += 1

# Event listeners
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    print('Loaded {} extensions'.format(extensionCounter))
    print('==========')

# Initialize bot
bot.run(config['discord_token'], bot=True, reconnect=True)
