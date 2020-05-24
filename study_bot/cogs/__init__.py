from .timer import Timer

def add_cogs(bot):
    timer_cog = Timer()
    timer_cog.schedule_all_from_db(bot)
    bot.add_cog(timer_cog)

__all__ = [
    "add_cogs"
]