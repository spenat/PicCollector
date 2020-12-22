import os
import json
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from .database_model import Subreddit, Picture, Base
from .gui_model import Model


dburl = Model.load_dburl()
# this_directory = os.path.dirname(os.path.realpath(__file__))


def create_database():
    # Base = declarative_base()
    dburl = Model.load_dburl()
    engine = create_engine(dburl, encoding="utf-8", echo=True)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


def database_exist():
    # return which(filename) is not None
    print(f'dburl: {dburl}')
    exists = os.path.exists("pcdb.sqlite")
    print(f'exists: {exists}')
    return exists

  
def create_subreddit(subreddit_name):
    subreddit = Subreddit()
    subreddit.name = ' '.join(subreddit_name.split('-')).title()
    subreddit.filename = subreddit_name + '.json'
    subreddit.url_key = subreddit_name
    return subreddit


def create_subs_from_cfg(filename, session):
    try:
        with open(filename, 'r+') as fo:
            subreddits = fo.read() 
        subreddits = [s for s in subreddits.split('\n') if s != '']
    except FileNotFoundError as exc:
        print(f'{__name__} got {exc}')
    db_subreddits = [] 
    for sub in subreddits:
        db_subreddits.append(create_subreddit(sub))
    session.add_all(db_subreddits)
    session.commit()
