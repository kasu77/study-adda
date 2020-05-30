from discord.ext.commands import Cog, command, Context
from discord import File

class AdminCog(Cog):
    """Admin commands meant to be used by admin of the bot"""
    
    @command(name='dumplog', hidden=True)
    async def dump_log(self, ctx: Context):
        if await ctx.bot.is_owner(ctx.author):
            await ctx.send(files=[File('bot.log')])

        else: await ctx.send('You are not authorized to use this command')