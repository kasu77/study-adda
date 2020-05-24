from discord.ext.commands import Cog, command, Context
from discord import Embed, Color

class Misc(Cog):

    @command()
    async def code(self, ctx: Context):
        """Get the link to view my source code"""

        await ctx.send(embed=Embed(
            title="Study Adda bot",
            description="**GitHub public repo:** https://github.com/quanta-kt/study-adda-bot",
            color=Color.green()
        ))