import os
import logging
import argparse
from db import utils
from db import database_manager
from gui.model import Model
from gui.controller import Controller
from gui.pic_collector import run
from db.gui_model import Model as DBModel


DBNAME = 'db/pcdb.sqlite'
cdir = os.path.dirname(os.path.realpath(__file__))


def load_subreddits(args):
    model = Model()
    subreddit_file = os.path.join(cdir, args.subreddit_file)
    subreddits = model.read_subreddits(subreddit_file)
    return subreddits


def scrape(args):
    if args.subreddits:
        subreddits = args.subreddits
    else:
        subreddits = load_subreddits(args)

    class PicConsole(DBModel, Controller):
        def __init__(self):
            self.root_directory = cdir
            super().__init__()
            self.load_model()

    ctrl = PicConsole()
    print(f'Scraping from {subreddits}')
    for subreddit in subreddits:
        ctrl.scrape_site(subreddit)


def create_db(args):
    print('Creating db')
    dbfilename = os.path.join(cdir, args.dbname)
    if os.path.exists(dbfilename):
        print(f'{dbfilename} already exists')
        overwrite = input('overwrite it? (y/n): ')
        if overwrite not in ['y', 'Y']:
            return
        print(f'deleting {dbfilename}')
        os.remove(dbfilename)
    utils.create_database()


def load_json(args):
    print('Loading json files')
    json_dir = os.path.join(cdir, 'pic_collector', 'json_files')
    dburl = DBModel.load_dburl().format(DBModel.db_directory)
    config_dir = os.path.join(cdir, 'config')
    dbmgr = database_manager.DatabaseManager(dburl, config_dir, echo=False)
    subreddits = dbmgr.get_subreddit_dict()
    for subreddit in subreddits:
        dbmgr.load_scrape_result_file(
            os.path.join(json_dir,
                         subreddits[subreddit]['json']),
            subreddit)


def main():
    parser = argparse.ArgumentParser(
        description='PicCollector from command prompt')
    parser.add_argument('--gui', dest='gui', action='store_true',
                        help='Start gui')
    parser.add_argument('--subreddits', dest='subreddits', type=str, nargs='+',
                        help='Subreddits you want to scrape and/or add')
    parser.add_argument('--subreddit-file', dest='subreddit_file', type=str,
                        default='config/subreddits.cfg',
                        help='File containing subreddits')
    parser.add_argument('--scrape', dest='scrape', action='store_true',
                        help='Scrape subreddits')
    parser.add_argument('--createdb', dest='create_db', action='store_true',
                        help='Create a sqlite database')
    parser.add_argument('--dbname', dest='dbname', action='store_true',
                        default=DBNAME,
                        help=f'Set database filename (default={DBNAME})')
    parser.add_argument('--loadjson', dest='load_json', action='store_true',
                        help='Load existing json files into database')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    if args.create_db:
        create_db(args)
    if args.load_json:
        load_json(args)
    if args.scrape:
        scrape(args)
    if args.gui:
        run()


if __name__ == '__main__':
    main()
