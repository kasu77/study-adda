from discord.ext import commands
from discord.ext.commands import Cog, command, Context, MissingPermissions
from discord.utils import get

class DndCog(Cog):

    ROLE_NAME = "Focus mode"

    @command(name='focusmode')
    async def dnd(self, ctx: Context, *args):
        """Turn focusmode on/off
        Example:
        focusmode on
        focusmode off
        """

        bot_perms = ctx.guild.me.permissions_in(ctx.channel)
        if not bot_perms.manage_roles:
            await ctx.send("Please give the 'Manage roles' permission to use this command")

        if len(args) != 1 or not args[0] in ['on', 'off']:
            await ctx.send('Usage: `focusmode [on | off]`')
            return

        role = get(ctx.guild.roles, name=DndCog.ROLE_NAME)
        if role == None:
            await ctx.send(f'{DndCog.ROLE_NAME} role is not set up. An admin must run `setupdnd` command to set it up')
            return

        if args[0] == 'on':
            await ctx.author.add_roles(role)
            await ctx.send('Your focus mode is now turned on!')
        else:
            await ctx.author.remove_roles(role)
            await ctx.send('Your focus mode is now turned off!')

    @command(name='setupdnd')
    @commands.has_permissions(manage_roles=True)
    async def setup_channels(self, ctx: Context, *channels):
        """Setup focus-mode
        Creates Focus mode role and forbids the role to read messages from given channels"""

        bot_perms = ctx.guild.me.permissions_in(ctx.channel)
        if not bot_perms.manage_roles:
            await ctx.send("Please give the 'Manage roles' permission to use this command")
        
        role = get(ctx.guild.roles, name=DndCog.ROLE_NAME)
        if role != None:
            await role.delete()

        role = await ctx.guild.create_role(name=DndCog.ROLE_NAME)

        channels = [ get(ctx.guild.channels, mention=it) for it in channels ]

        if None in channels:
            await ctx.send('One or more channels are invalid')

        for channel in channels:
            await channel.set_permissions(role, read_messages=False)

        await ctx.send(f'{DndCog.ROLE_NAME} role set up complete!')

    @setup_channels.error
    async def setup_channels_error(self, ctx: Context, e: Exception):
        if isinstance(e, MissingPermissions):
            await ctx.send(str(e))