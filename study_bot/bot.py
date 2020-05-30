from discord.ext.commands import Bot
import json
import logging

from . import cogs
from .data import Repository

#Setup logging
log = logging.getLogger('botlog')
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
log.addHandler(handler)

class StudyBot(Bot):

    def __init__(self):
        super().__init__(command_prefix='.')
        self.repository = Repository()
        cogs.add_all(self)

    async def on_ready(self):
        log.info('Bot: on_ready')

    async def close(self):
        await super().close()
        self.repository.close()
        log.info('Bot exited')

def main():
    """Entry point of the bot"""

    log.info('******Starting up bot******')
    
    with open('config.json') as fp:
        config = json.loads(fp.read())
    StudyBot().run(config['token'])