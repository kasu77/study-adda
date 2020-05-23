from discord.ext.commands import Cog, command
from discord.ext.commands import Context
from discord import User, TextChannel
import re
import asyncio

class Timer(Cog):
     
    @command('timer')
    async def timer(self, ctx: Context, *time):
        """Set a new timer
        Pass it the duration in format Xh Xm Xs with all params optional"""

        time = ' '.join(time)

        if time == '' or time.isspace():
            await ctx.send('You gotta say how much time to wait kiddo')
            return

        duration_pattern = re.compile('^((?P<hours>\\d+)h)?(\\s*(?P<minutes>\\d*)m)?(\\s*(?P<seconds>\\d+)s)?$')
        match = duration_pattern.match(time)
         
        if match == None:
           await ctx.send("Lol nerd, does that looks like a proper time format to you? Read help lol")
           return

        duration_dict = match.groupdict()

        def value_or_zero(val):
            return int(val) if val != None else 0

        sec = value_or_zero(duration_dict['seconds'])
        minutes = value_or_zero(duration_dict['minutes'])
        hours = value_or_zero(duration_dict['hours'])
        
        duration = sec + (minutes * 60) + (hours * 60)

        if duration == 0:
            await ctx.send('You want me to wait zero seconds lol? oK tHeN smh')
            return 0

        await self.schedule(duration, ctx.author, ctx.channel)

        await ctx.send(f"There ya go. I'll ping you in {hours}h {minutes}m {sec}s :>")

    async def schedule(self, duration: int, owner: User, channel: TextChannel):
        """Schedules a timer task for given duration"""

        async def timer_task():
            await asyncio.sleep(duration)
            await channel.send(f"{owner.mention} Yo you there? Your timer is done, don't be dead!")

        asyncio.create_task(timer_task())