import os
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database_manager import DatabaseManager
from .database_model import Base

from pic_collector import settings


class Model:

    page = 1
    subreddit = 'pics'
    image_data = {}
    db_directory = os.path.dirname(os.path.realpath(__file__)) + '/'
    debug = False
    json_dir = os.path.join('pic_collector', 'json_files')
    dburl_file = "dburl.json"
    db_type = "sqlite"
    options_file = 'options.json'
    images_dir = settings.IMAGES_STORE

    def __init__(self):
        self.subreddits_filename = os.path.join(self.root_directory, 'config', "subreddits.cfg")
        self.options_file = os.path.join(self.root_directory, 'config', self.options_file)
        self.dburl = Model.load_dburl()
        if self.db_type == 'sqlite':
            self.dburl = self.dburl.format(self.db_directory)
        self.log(self.dburl)
        self.dbmgr = DatabaseManager(self.dburl, os.path.join(self.root_directory, 'config'), echo=False)

    def load_model(self):
        self.load_options()
        self.subreddits = self.dbmgr.get_subreddit_dict()
        self.log(self.subreddits)
        self.subreddit = sorted(list(self.subreddits))[0]

    def load_imagedata(self):
        self.page = 1
        success = True
        thumbs = self.dbmgr.get_thumbs(self.subreddit)
        json_filename = os.path.join(self.root_directory, self.json_dir,
                                     self.subreddits[self.subreddit]['json'])
        if not thumbs and os.path.exists(json_filename):
            self.dbmgr.load_scrape_result_file(json_filename, self.subreddit)
            thumbs = self.dbmgr.get_thumbs(self.subreddit)
        self.image_data = [{
            "image_urls": [t.image_url],
            "description":
            t.description,
            "images": [{
                "url": t.image_url,
                "path": t.path,
                "checksum": t.checksum
            }],
        } for t in thumbs]
        return success

    def load_options(self):
        with open(self.options_file) as file:
            self.options = json.load(file)

    def log(self, text):
        print(f'log : {text}')
        # pass

    @classmethod
    def load_dburl(cls):
        with open(cls.db_directory + cls.dburl_file, 'r') as file:
            dburl = json.load(file)[cls.db_type]
        return dburl
