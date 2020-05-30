from discord.ext.commands import Cog, command, Context, Bot
from discord import User, TextChannel, Message, Embed, Color
import asyncio
import re
import time
import sys
from datetime import timedelta
import logging

from ..data import Timer, Repository

log = logging.getLogger('botlog')

class TimerCog(Cog):

    def __init__(self):
        super().__init__()

        #A dictionary of asyncio tasks corresponding to scheduled timers
        #Key: Timer.id; value: Task object
        self.timer_tasks = dict()

        #A flag indicating weather timers from  db were scheduled
        self.db_scheduled = False

    def _inject(self, bot):
        """This is overriden to save the instance of the bot"""

        log.info('Injecting TimerCog')
        
        self.bot = bot
        self.dao = bot.repository.timers_dao
        return super()._inject(bot)

    @Cog.listener()
    async def on_connect(self):
        log.info('TimerCog: on_connect')
        if not self.db_scheduled:
            self.db_scheduled = True
            await self.schedule_timers_from_db(self.bot)
     
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
        
        duration = sec + (minutes * 60) + (hours * 60 * 60)

        if duration == 0:
            await ctx.send('You want me to wait zero seconds lol? oK tHeN smh')
            return 0

        timer = Timer(
            time = int(time.time()) + duration,
            user_id = ctx.author.id,
            channel_id = ctx.channel.id,
            guild_id = ctx.guild.id,
            reason = reason
        )

        self.dao.add_timer(timer)
        await self.schedule_timer(timer, ctx.bot)
        
        await ctx.send(f"There ya go. I'll ping you in {hours}h {minutes}m {sec}s :>")
        log.info('Started timer id=' + timer.id)

    @command(name='showtimers', aliases=['timers', 'st'])
    async def show_timers(self, ctx: Context):
        """Lists the timers in this channel"""

        def format_duration(unix_time):
            duration = unix_time - int(time.time()) #Round to int as we don't have to deal with milliseconds component
            return str(timedelta(seconds=duration))

        embed_content = ""
        count = 0
        for timer in self.dao.get_all_timers_for_channel(ctx.channel.id, ctx.guild.id):
            embed_content += f"**\\[#{timer.id}\\]** <@{timer.user_id}> ({format_duration(timer.time)}) - {timer.reason}\n"
            count += 1

        embed = Embed(
            title=f"{count} timers running",
            description=embed_content
        )

        await ctx.send(embed=embed)

    @command(name='mytimers', aliases=['mt'])
    async def user_timers(self, ctx: Context):
        """View your timers
        Shows all the timers in the channel that were started by you"""

        def format_duration(unix_time):
            duration = unix_time - int(time.time()) #Round to int as we don't have to deal with milliseconds component
            return str(timedelta(seconds=duration))

        embed_content = ""
        count = 0
        for timer in self.dao.get_user_timers_for_channel(ctx.author.id, ctx.channel.id, ctx.guild.id):
            embed_content += f'**\\[#{timer.id}\\]** ({format_duration(timer.time)}) - {timer.reason}\n'
            count += 1

        embed = Embed(
            title=f"You have {count} timers running",
            description=embed_content,
            color=Color.green()
        )

        await ctx.send(embed=embed)

    @command(name='canceltimer', aliases=['ct', 'dismis'])
    async def cancel_timer(self, ctx: Context, *args):
        """Cancel a timer
        Cancels a timer with given id. The timer must be started by you"""

        if len(args) != 1:
            await ctx.send('Please pass id of the timer you wish to cancel. Get the ids using "mytimers" command')
            return

        try:
            to_cancel = int(args[0])
        except ValueError:
            await ctx.send("That doesn't looks like a timer id to me ;-;")
            return

        timer = self.dao.get_timer_by_id(to_cancel)

        if timer == None:
            await ctx.send("Are you kidding? there's no such timer in my records")
            return

        if timer.user_id != ctx.author.id:
            await ctx.send("That timer doesn't belong to you. You can only cancel timers started by you")
            return

        #Cancel and delete the task and timer
        self.timer_tasks[timer.id].cancel()
        del self.timer_tasks[timer.id]
        self.dao.finish_timer(timer)

        await ctx.send(f'Canceled timer #{timer.id}')
        log.infot('Canceled timer id=' + timer.id)

    async def schedule_timer(self, timer: Timer, bot: Bot):
        """Schedules a timer as a task"""

        async def timer_task():
            #Wait
            await bot.wait_until_ready()
            await asyncio.sleep(max(timer.time - time.time(), 0))

            #Trigger
            channel = bot.get_guild(timer.guild_id).get_channel(timer.channel_id)
            await channel.send(f"<@{timer.user_id}> Yo you there? Your timer called \"{timer.reason}\" is done, don't be dead!")

            log.info("Finishing timer id=" + timer.id)

            #Cleanup
            try:
                del self.timer_tasks[timer.id]
            except KeyError:
                log.error("KeyError while cleaning up timer id=" + timer.id)

            self.dao.finish_timer(timer)

        #Check if the timer with the same id is already present in the dict
        if timer.id in self.timer_tasks.keys():
            log.warn('Tried to re-schedule timer. id=' + timer.id)
            return

        self.timer_tasks[timer.id] = asyncio.create_task(timer_task())

    async def schedule_timers_from_db(self, bot: Bot):
        """Schedules all timers in db"""

        log.info('Scheduling timers from db.')

        for timer in self.dao.get_all_timers():
            await self.schedule_timer(timer, bot)
