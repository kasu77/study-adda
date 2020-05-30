from typing import List, Union
import sys
import logging

from .orm import Timer

log = logging.getLogger('botlog')

class TimersDao():
    def __init__(self, db_session):
        self.db_session = db_session

    def close(self):
        """Closes connection with db"""

        self.db_session.commit()
        self.db_session.close()

    def add_timer(self, timer: Timer):
        """Add timer to db"""

        self.db_session.add(timer)

        try:
            self.db_session.commit()
        except Exception as e:
            log.error(f'Error while adding new timer to db: {e}. Rolling back')
            self.db_session.rollback()

    def get_all_timers_for_channel(self, channel_id: int, guild_id: int) -> List[Timer]:
        """Returns a list of all active timers in the given channel of the guild"""

        return self.db_session.query(Timer)\
            .filter(Timer.guild_id == guild_id)\
            .filter(Timer.channel_id == channel_id)\
            .all()

    def get_user_timers_for_channel(self, user_id: int, channel_id: int, guild_id: int) -> List[Timer]:
        """Returns a list of all the timers in the channel belonging to given user"""

        return self.db_session.query(Timer)\
            .filter(Timer.guild_id == guild_id)\
            .filter(Timer.channel_id == channel_id)\
            .filter(Timer.user_id == user_id)\
            .all()

    def get_timer_by_id(self, id: int) -> Timer:
        """Returns the timer referenced by the given id"""

        return self.db_session.query(Timer)\
            .filter(Timer.id == id)\
            .first()

    def finish_timer(self, timer: Timer):
        """Removes a timer from db"""

        self.db_session.delete(timer)

        try:
            self.db_session.commit()
        except Exception as e:
            log.error(f'Error while deleting timer from db: {e}. Rolling back')
            self.db_session.rollback()
    
    def get_all_timers(self) -> List[Timer]:
        """Returns the list of all timers in db"""

        return self.db_session.query(Timer)\
            .all()