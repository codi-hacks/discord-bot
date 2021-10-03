from discord.ext import commands
# https://github.com/jsvine/markovify
import markovify
# https://www.nltk.org/api/nltk.html
import nltk
import os
import random
import re
import yaml

config_file = os.path.join(os.path.dirname(__file__), '..', 'config.yml')
with open(config_file, 'r') as file:
  config = yaml.safe_load(file)

class Markov(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Place to store all the corpus file (in the extensions dir with this file in this case)
        corpus_dir = os.path.dirname(__file__)
        # Primary corpus is the user chat log
        self.log_file = os.path.join(corpus_dir, 'markov.log')

        # Static corpus files that get loaded and processed
        models = []
        # Weighted value of each corpus. A corpus with more
        # weight has a bigger influence on markov chains.
        weights = []

        # Check if we should be logging and learning new phrases
        if config['markov.learn']:
            # Create a chat log corpus if one doesn't exist
            self.touch_log_file()
            # Load in the log file as a corpus
            with open(self.log_file) as f:
                models.append(markovify.NewlineText(f.read()))
                # Log file has more influence than the static corpus files
                weights.append(2.0)

        # Import all *.corpus files into the model
        for i in os.listdir(corpus_dir):
            if i.endswith('.corpus') and os.path.isfile(os.path.join(corpus_dir, i)):
                print('[markov.info] Loading corpus "{}"'.format(os.path.join(corpus_dir, i)))
                with open(os.path.join(corpus_dir, i)) as f:
                    models.append(markovify.NewlineText(f.read()))
                    weights.append(1.0)

        self.model = markovify.combine(models)

    @commands.command()
    async def markov(self, ctx):
        """Chat with you"""
        # Remove command prefix from string
        text = ' '.join(ctx.message.clean_content.strip().split(' ')[1:])
        seed_text = self.extract_seed_text(text)
        if len(seed_text) >= 3:
            try:
                await ctx.channel.send(self.model.make_sentence_with_start(seed_text, False))
            except Exception:
                await ctx.channel.send(self.model.make_sentence())
        else:
            await ctx.channel.send(self.model.make_sentence())

    @commands.Cog.listener()
    async def on_message(self, msg):
        # Ignore own messages
        if msg.author == self.bot.user:
            return

        text = msg.clean_content.strip()
        if self.contains_garbage(text):
            return

        sentences = nltk.tokenize.sent_tokenize(text)
        if len(sentences) < 1:
            return

        self.append_to_log_file(sentences)
        # Let's consider sparking up a conversation if this is a channel in which
        # we're allowed to talk unprompted. Private channels bypass this check.
        if msg.channel.type == 'text' and not msg.channel.name in config['markov.channels']:
            return
        # Check probability to see if we should respond
        probability = config['markov.probability']
        if not isinstance(probability, int) and not isinstance(probability, float):
            print('[markov.error] Invalid value given in config file for "markov.probability"')
            return
        if probability * 100 <= random.randint(0, 10000):
            return

        # Generate message based on a portion of the user's sent
        if len(sentences[0]) >= 3:
            seed_text = self.extract_seed_text(sentences[0])
            print('[markov.debug] Text trigger - "{}"'.format(seed_text))
            try:
                await msg.channel.send(self.model.make_sentence_with_start(seed_text, False))
            except Exception:
                return

    # Pass an array of sentences to append to the end of the log corpus
    def append_to_log_file(self, sentences):
        self.touch_log_file()
        if config['markov.learn']:
            with open(self.log_file, 'a') as f:
                for sentence in sentences:
                    # Ignore one-word sentences
                    if len(sentence.split(' ')) > 1:
                        print('[markov.debug] Logging "{}"'.format(sentence))
                        f.write(sentence + '\n')

    # Create a chat log corpus if one doesn't exist
    def touch_log_file(self):
        if config['markov.learn']:
            if not os.path.exists(self.log_file):
                print('[markov.info] Creating markov.log')
                with open(self.log_file, 'w') as f:
                    # Some initial seed data is needed for markovify to read the corpus
                    f.write('Hello World!\nGoodbye cruel world!\n')

    # Return True if any non-language text is found in the
    # string that could lower the quality of markov chain models
    def contains_garbage(self, text):
        patterns = [
            # Check for URLS
            r'(https?://\S+)',
            # Backticks could indicate a block of code or similar garbage
            '`',
            # Potential user commands
            r'^(\.|\@|\!|,)',
            # Other stuff that looks like code
            r'(::|{|}|\(|\)|\\|\;|=)',
            '<<'
        ]
        for pattern in patterns:
            if re.search(pattern, text):
                return True
        return False

    # Markovify only accepts 2 words as a seed for
    # a markov chain. Use last 2 words as seed text.
    def extract_seed_text(self, text):
        words = []
        for word in text.split(' ')[-2:]:
            if len(word) > 1:
                words.append(word)
        return re.sub('(\.|\?|!)*$', '', ' '.join(words))


def setup(bot):
    # Update natural language processor at runtime for some reason :/
    nltk.download('punkt')
    # Initialize an instance of the Markov extension class defined above
    bot.add_cog(Markov(bot))
