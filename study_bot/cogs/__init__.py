from .timer import Timer

def add_cogs(bot):
    bot.add_cog(Timer())

__all__ = [
    "add_cogs"
]