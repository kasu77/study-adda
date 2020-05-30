from .timer import TimerCog
from .misc import Misc
from .donotdisturb import DndCog
from .admin import AdminCog

def add_all(bot):
    """Add all available cogs to the bot"""
    
    bot.add_cog(TimerCog())
    bot.add_cog(DndCog())
    bot.add_cog(Misc())
    bot.add_cog(AdminCog())

all = [
    'add_all',
]