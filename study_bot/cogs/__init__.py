from .timer import TimerCog
from .misc import Misc

def add_all(bot):
    """Add all available cogs to the bot"""
    
    bot.add_cog(TimerCog())
    bot.add_cog(Misc())

all = [
    'add_all',
]