from .timer import Timer
from .misc import Misc

def add_cogs(bot):
    #Timer
    timer_cog = Timer()
    timer_cog.schedule_all_from_db(bot)
    bot.add_cog(timer_cog)

    #Misc
    bot.add_cog(Misc())

__all__ = [
    "add_cogs"
]