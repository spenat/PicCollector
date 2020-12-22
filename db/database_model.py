from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


Base = declarative_base()


class Subreddit(Base):
    __tablename__ = 'subreddit'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    filename = Column(String)
    url_key = Column(String)


class Picture(Base):
    __tablename__ = 'picture'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now())
    checksum = Column(String, unique=True)
    image_url = Column(String)
    description = Column(String)
    status = Column(String)
    path = Column(String)
    subreddit_id = Column(Integer, ForeignKey('subreddit.id'))
    subreddit = relationship("Subreddit", backref="subreddit")
