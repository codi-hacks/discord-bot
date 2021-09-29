from discord.ext import commands
# https://github.com/jsvine/markovify
import markovify
# https://www.nltk.org/api/nltk.html
import nltk
import os
import re

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

        # Create a chat log corpus if one doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'): pass

        # Import all *.corpus files into the model
        with open(self.log_file) as f:
            models.append(markovify.NewlineText(f.read()))
            # Log file has more influence than the static corpus files
            weights.append(2.0)
        for i in os.listdir(corpus_dir):
            if i.endswith('.corpus') and os.path.isfile(os.path.join(corpus_dir, i)):
                print('[markov.info] Loading corpus "{}"'.format(os.path.join(corpus_dir, i)))
                with open(os.path.join(corpus_dir, i)) as f:
                    models.append(markovify.NewlineText(f.read()))
                    weights.append(1.0)

        self.model = markovify.combine(models)

    # Pass an array of sentences to append to the end of the log corpus
    def append_to_log_file(self, sentences):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w'): pass
        with open(self.log_file, 'a') as f:
            for sentence in sentences:
                print('[markov.debug] Logging "{}"'.format(sentence))
                f.write(sentence + '\n')

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

    @commands.command()
    async def markov(self, ctx):
        """Chat with you"""
        #print('.markov clean_content: "{}"'.format(ctx.message.clean_content))
        await ctx.channel.send(self.model.make_sentence())

    @commands.Cog.listener()
    async def on_message(self, ctx):
        # Ignore own messages
        if ctx.author == self.bot.user:
            return
        text = ctx.clean_content
        if self.contains_garbage(text):
            return
        sentences = nltk.tokenize.sent_tokenize(text)
        self.append_to_log_file(sentences)

def setup(bot):
    # Update natural language processor at runtime for some reason :/
    nltk.download('punkt')
    # Initialize an instance of the Markov extension class defined above
    bot.add_cog(Markov(bot))
