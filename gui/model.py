import json
import os
import traceback

from pic_collector import settings


class Model:

    page = 1
    subreddit = 'pics'
    image_data = {}
    json_dir = os.path.join('pic_collector', 'json_files')
    debug = False
    options_file = 'options.json'
    images_dir = settings.IMAGES_STORE

    def load_model(self):
        self.subreddits_filname = os.path.join(self.root_directory, 'config',
                                               "subreddits.cfg")
        self.options_file = os.path.join(self.root_directory, 'config',
                                         self.options_file)
        self.load_options()
        self.subreddits = self.read_subreddits(self.subreddits_filname)
        self.log(self.subreddits)
        self.subreddit = sorted(list(self.subreddits))[0]

    def read_subreddits(self, filename):
        try:
            with open(filename, 'r+') as fo:
                subreddits = fo.read()
            subreddits = [s for s in subreddits.split('\n') if s != '']
        except FileNotFoundError as exc:
            self.log(f'Got exception {exc} when opening file: {filename}')
            traceback.print_exc()
        subreddits = {
            ' '.join(subreddit.split('-')).title(): {
                'json': subreddit + '.json',
                'url_key': subreddit
            }
            for subreddit in subreddits
        }
        self.log(f'{subreddits}')
        return subreddits

    def load_imagedata(self):
        self.page = 1
        filename = os.path.join(self.root_directory, self.json_dir,
                                self.subreddits[self.subreddit]['json'])
        self.log(f'filename: {filename}')
        success = False
        try:
            with open(filename, 'r') as file:
                self.image_data = json.load(file)
            self.clean_image_data()
            success = True
        except Exception as exc:
            self.log(f"Exception noted: {exc}")
            self.log(traceback.format_exc())
            self.image_data = {}

        return success

    def clean_image_data(self):
        to_be_removed = []
        for image_meta in self.image_data:
            images = image_meta['images']
            if len(image_meta['images']) == 0:
                to_be_removed.append(image_meta)
        for im in to_be_removed:
            self.image_data.remove(im)

    def load_options(self):
        with open(self.options_file) as file:
            self.options = json.load(file)

    def log(self, text):
        print(f'log : {text}')
