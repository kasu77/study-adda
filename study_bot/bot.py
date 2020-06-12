from discord.ext.commands import Bot
import json

from . import cogs
from .data import Repository

class StudyBot(Bot):

    def __init__(self):
        super().__init__(command_prefix='.')
        self.repository = Repository()
        cogs.add_all(self)

    async def on_ready(self):
        print('Bot loaded')

    async def close(self):
        await super().close()
        self.repository.close()
        print('Bot exited')

def main():
    """Entry point of the bot"""
    
    with open('config.json') as fp:
        config = json.loads(fp.read())
    StudyBot().run(config['NzE5OTI0MjY4NDA5ODE1MDUx.XuNUFg.OPkxPBuMI9R-0iy7Ud2FVAQA5WM'])
