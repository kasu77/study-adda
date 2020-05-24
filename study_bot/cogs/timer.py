from discord.ext.commands import Cog, command, Context, Bot
from discord import User, TextChannel, Message, Embed
import asyncio
import re
import time
from datetime import timedelta

from .. import repository

class Timer(Cog):

    def __init__(self):
        super().__init__()
        self.repo = repository.TimersRepo()
     
    @command('timer')
    async def timer(self, ctx: Context, *args):
        """Set a new timer
        Pass it the duration in format XhXmXs with all params optional and a reason for the timer"""

        if len(args) < 2:
            await ctx.send("That's not how you use this command. Use help!")
            return

        time_arg = args[0]
        reason = ' '.join(args[1:])

        if time_arg == '' or time_arg.isspace():
            await ctx.send('You gotta say how much time_arg to wait kiddo')
            return

        duration_pattern = re.compile('^((?P<hours>\\d+)h)?((?P<minutes>\\d+)m)?((?P<seconds>\\d+)s)?$')
        match = duration_pattern.match(time_arg)
         
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

        self.new_timer(
            ctx.bot,            
            repository.Timer(
                time = int(time.time()) + duration,
                user_id = ctx.author.id,
                channel_id = ctx.channel.id,
                guild_id = ctx.guild.id,
                reason = reason
            )
        )

        await ctx.send(f"There ya go. I'll ping you in {hours}h {minutes}m {sec}s :>")

    @command(name='showtimers')
    async def show_timers(self, ctx: Context):
        """Lists the timers in this channel"""

        def format_duration(unix_time):
            duration = unix_time - int(time.time()) #Round to int as we don't have to deal with milliseconds component
            return str(timedelta(seconds=duration))

        embed_content = ""
        count = 0
        for timer in self.repo.get_all_timers_for_channel(ctx.channel.id, ctx.guild.id):
            embed_content += f"**[{count + 1}]** <@{timer.user_id}> ({format_duration(timer.time)}) - {timer.reason}"
            count += 1

        embed = Embed(
            title=f"{count} timers running",
            description=embed_content
        )

        await ctx.send(embed=embed)

    def new_timer(self, bot: Bot, timer: repository.Timer):
        """Adds a timer to db and schedules it"""

        self.repo.add_timer(timer)
        self.schedule(bot, timer)

    def schedule(self, bot: Bot, timer: repository.Timer):
        """Schedules a timer task for given duration"""

        async def timer_task():
            await asyncio.sleep(timer.time - time.time())
            channel = bot.get_guild(timer.guild_id).get_channel(timer.channel_id)
            await channel.send(f"<@{timer.user_id}> Yo you there? Your timer called \"{timer.reason}\" is done, don't be dead!")

        asyncio.create_task(timer_task())

    def schedule_all_from_db(self, bot: Bot):
        """Loads all timers from db and schedules them"""

        for timer in self.repo.get_all_timers():
            self.schedule(bot, timer)