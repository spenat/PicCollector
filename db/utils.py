import os
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database_model import Subreddit, Base
from .gui_model import Model


dburl = Model.load_dburl()


def create_database(db_type='sqlite'):
    # Base = declarative_base()
    dburl = Model.load_dburl()
    if db_type == 'sqlite':
        db_directory = os.path.dirname(os.path.realpath(__file__)) + '/'
        dburl = dburl.format(db_directory)
    engine = create_engine(dburl, encoding="utf-8", echo=True)
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)


def database_exist(root_dir):
    exists = os.path.exists(os.path.join(root_dir, 'db', "pcdb.sqlite"))
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
        traceback.print_exc()
    db_subreddits = []
    q_subreddits = [sub.url_key for sub in session.query(Subreddit).all()]
    for sub in subreddits:
        if sub not in q_subreddits:
            db_subreddits.append(create_subreddit(sub))
    session.add_all(db_subreddits)
    session.commit()
