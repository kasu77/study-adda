from sqlalchemy import Column, Integer, String
from .repository import Base

class Timer(Base):
    __tablename__ = 'timer'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)
    channel_id = Column(Integer, nullable=False)
    guild_id = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)