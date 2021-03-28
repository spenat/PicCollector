import os
import falcon
from pathlib import Path
from falcon_cors import CORS
from db import utils
from db import database_manager
from gui.controller import Controller
from db.gui_model import Model as DBModel


class Subreddit:
    def __init__(self, dbmgr):
        self.dbmgr = dbmgr
        self.subreddits = self.dbmgr.get_subreddit_dict()
        self.total = sum([int(self.subreddits[s]["quantity"]) for s in self.subreddits])

    def on_get(self, req, resp, name):
        if name == 'total_images':
            resp.media = {"total": self.total}
        elif name in list(self.subreddits):
            resp.media = self.subreddits[name]
        else:
            resp.media = list(self.subreddits)


class Picture:
    def __init__(self, dbmgr):
        self.dbmgr = dbmgr

    def on_get(self, req, resp, subreddit_name, offset, page_size):
        _images = [{
                "image_urls": [t.image_url],
                "description":
                t.description,
                "images": [{
                    "url": t.image_url,
                    "path": t.path,
                    "checksum": t.checksum
                }],
            } for t in self.dbmgr.get_thumbs(subreddit_name)]
        if offset + page_size < len(_images):
            resp.media = _images[offset:offset + page_size]
        elif offset < len(_images):
            resp.media = _images[offset:]
        else:
            resp.media = []


cors = CORS(allow_origins_list=['http://localhost:8080'],
            allow_all_headers=True,
            allow_all_methods=True)

cdir = Path(__file__).parent.parent
dburl = DBModel.load_dburl().format(DBModel.db_directory)
config_dir = os.path.join(cdir, 'config')
dbmgr = database_manager.DatabaseManager(dburl, config_dir, echo=False)

api = falcon.API(middleware=[cors.middleware])
api.add_route('/subreddit/{name}', Subreddit(dbmgr))
api.add_route('/pics/{subreddit_name}/{offset:int}/{page_size:int}', Picture(dbmgr))
