from discord.ext.commands import Bot
import json

from . import cogs

study_bot = Bot(".")
cogs.add_cogs(study_bot)

def main():
    """Entry point of the bot"""
    
    with open('config.json') as fp:
        config = json.loads(fp.read())
    study_bot.run(config['token'])