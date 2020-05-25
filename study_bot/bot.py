from discord.ext.commands import Bot
import json

from . import cogs

class StudyBot(Bot):

    def __init__(self):
        super().__init__(command_prefix='.')
        self.timer_cog = cogs.Timer()
        self.add_cog(self.timer_cog)
        self.add_cog(cogs.Misc())

    async def on_ready(self):
        self.timer_cog.start_ticker(self)
        print('Bot loaded')

    async def close(self):
        await super().close()
        self.timer_cog.close()
        print('Bot exited')

def main():
    """Entry point of the bot"""
    
    with open('config.json') as fp:
        config = json.loads(fp.read())
    StudyBot().run(config['token'])