import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_path = 'sqlite:////' + os.path.join(os.path.abspath(os.curdir), 'database.db')
engine = create_engine(db_path)
DBSession = sessionmaker(bind=engine)

Base = declarative_base()

from .orm import Timer
from .timers_dao import TimersDao

Base.metadata.create_all(engine)

class Repository:
    def __init__(self):
        self.db_session = DBSession()
        self.timers_dao = TimersDao(self.db_session)

    def close(self):
        self.db_session.commit()
        self.db_session.close()