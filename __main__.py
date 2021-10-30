import argparse
import logging
import os
import pprint
import json

from db import utils
from db import database_manager
from db.gui_model import Model as DBModel
from gui.controller import Controller
from gui.model import Model
from gui.pic_collector import run, PicConsole

DBNAME = 'db/pcdb.sqlite'
cdir = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(f'{__file__} {__name__}')


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

    model = DBModel(cdir)
    controller = Controller(model)
    pc = PicConsole(model, controller)
    logger.info(f'Scraping from {subreddits}')
    for subreddit in subreddits:
        pc.scrape_site(subreddit)


def generate_cs(filename):
    return filename[:8]


def create_image_data(filename):
    image_data = {
        'description': 'orphan-' + filename[:-4],
        'image_urls': [''],
        'images': [{
            'url': '',
            'path': 'full/' + filename,
            'checksum': generate_cs(filename),
            'status': 'downloaded',
        }]
    }
    return image_data


def find_orphans(args):
    model = DBModel(cdir)
    model.load_model()
    logger.info(f'model.images_dir: {model.images_dir}')
    files = os.listdir(model.images_dir + '/full')

    if 'Orphans' not in model.subreddits:
        logger.info(f'no subreddit : {model.subreddits}')
        add_subreddit('orphans')
    nof = len(files)
    logger.info(f'nof: {nof}')
    orphans = []
    for filename in files:
        result = model.dbmgr.look_for_picture('full/' + filename)
        if result is None:
            orphans.append(filename)
    noo = len(orphans)
    image_data = []
    for orphan in orphans:
        image_data.append(create_image_data(orphan))
    with open('orphans.json', 'w') as file:
        json.dump(image_data, file, indent=4)
    model.dbmgr.load_scrape_result_file('orphans.json', 'Orphans')
    logger.info(f'Added {noo} orphans')


def add_subreddit(url_key):
    model = DBModel(cdir)
    subreddit = utils.create_subreddit(url_key)
    s = model.dbmgr.session()
    s.add(subreddit)
    s.commit()
    s.close()


def show_options():
    model = DBModel(cdir)
    model.load_options()
    options = model.options
    logger.info(f'Options :')
    pprint.pprint(options)


def create_db(args):
    logger.info('Creating db')
    dbfilename = os.path.join(cdir, args.dbname)
    if os.path.exists(dbfilename):
        logger.info(f'{dbfilename} already exists')
        overwrite = input('overwrite it? (y/n): ')
        if overwrite not in ['y', 'Y']:
            return
        logger.info(f'deleting {dbfilename}')
        os.remove(dbfilename)
    utils.create_database()


def load_json(args):
    logger.info('Loading json files')
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
        description='PicCollector')
    parser.add_argument('--gui', dest='gui', action='store_true',
                        help='Start gui')
    parser.add_argument('--orphans', dest='orphans', action='store_true',
                        help='Find orphans')
    parser.add_argument('--show-options', dest='show_options', action='store_true',
                        help='Show options')
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
    if args.orphans:
        find_orphans(args)
    if args.show_options:
        show_options()


if __name__ == '__main__':
    main()
