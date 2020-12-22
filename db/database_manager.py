import json
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
from . import utils
from .database_model import Subreddit, Picture

# This is the database manager. Its a collection of useful database queries


class DatabaseManager():
    def __init__(self, dburl, echo=True):
        self.dburl = dburl
        engine = create_engine(dburl, encoding="utf-8", echo=echo)
        session_factory = sessionmaker(bind=engine)
        self.session = scoped_session(session_factory)

    def get_thumbs(self, subreddit):
        s = self.session()
        subreddit = s.query(Subreddit).filter(Subreddit.name == subreddit).one_or_none()
        if subreddit:
            thumbs_query = s.query(Picture).filter(
                Picture.subreddit_id == subreddit.id)
        else:
            return None
        s.close()
        return thumbs_query.order_by(Picture.id).all()

    def get_subreddit_dict(self):
        s = self.session()
        s_query = s.query(Subreddit).all()
        if not s_query:
            utils.create_subs_from_cfg('.subreddits.cfg', s)
            s_query = s.query(Subreddit).all()
        subreddit_dict = {
            sub.name: {
            'json': sub.filename,
            'url_key': sub.url_key
            }
            for sub in s_query
        }
        return subreddit_dict

    def load_file(self, filename, subreddit):
        with open(filename, 'r') as file:
            image_data = json.load(file)
        s = self.session()
        subreddit = s.query(Subreddit).filter(
            Subreddit.name == subreddit).one_or_none()
        pictures = []
        checksums = []
        for image in image_data:
            if len(image['images']) != 0:
                duplicate = s.query(Picture).filter(Picture.checksum == image['images'][0]['checksum']).all()
                if duplicate or image['images'][0]['checksum'] in checksums: # is not None:
                    duplicate = None
                    continue
            else:
                continue
            try:
                picture = Picture()
                picture.checksum = image['images'][0]['checksum']
                checksums.append(picture.checksum)
                picture.description = image['description']
                picture.image_url = image['image_urls'][0]
                picture.status = image['images'][0]['status']
                picture.path = image['images'][0]['path']
                picture.subreddit_id = subreddit.id
                pictures.append(picture)
            except Exception as exc:
                self.log(f'got exception when adding file: {exc}')
        s.add_all(pictures)
        s.commit()
        s.close()