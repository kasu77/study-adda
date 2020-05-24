from typing import List
import os
import time
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Timer(Base):
    __tablename__ = 'timer'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    channel_id = Column(Integer, nullable=False)
    guild_id = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)

db_path = 'sqlite:////' + os.path.join(os.path.abspath(os.curdir), 'database.db')
engine = sqlalchemy.create_engine(db_path)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sqlalchemy.orm.sessionmaker(bind=engine)

class TimersRepo():
    def __init__(self):
        self.db_session = DBSession()


    def add_timer(self, timer: Timer):
        """Add timer to db"""

        self.db_session.add(timer)
        self.db_session.commit()

    def get_all_timers_for_channel(self, channel_id: int, guild_id: int) -> List[Timer]:
        """Returns a list of all active timers in the given channel of the guild"""

        return self.db_session.query(Timer)\
            .filter(Timer.guild_id == guild_id)\
            .filter(Timer.channel_id == channel_id)\
            .filter(Timer.time > int(time.time()))\
            .all()
    
    def get_all_timers(self) -> List[Timer]:
        """Returns a list of ALL the active timers in the db"""

        return self.db_session.query(Timer)\
            .filter(Timer.time > int(time.time()))\
            .all()