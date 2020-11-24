import json
import os


class PCModel:

    page = 1
    subreddit = 'pics'
    image_data = {}
    json_dir = 'pic_collector/json_files'
    debug = False

    def load_model(self):

        self.subreddits_filname = os.path.join(self.this_directory,
                                               ".subreddits.cfg")
        self.subreddits = self.read(self.subreddits_filname)
        self.log(self.subreddits)
        self.subreddit = sorted(list(self.subreddits))[0]

    def read(self, filename):
        try:
            with open(filename, 'r+') as fo:
                subreddits = fo.read()
            subreddits = [s for s in subreddits.split('\n') if s != '']
        except FileNotFoundError as e:
            self.log(f'{e}')
        subreddits = {
            ' '.join(subreddit.split('-')).title(): {
                'json': subreddit + '.json',
                'url_key': subreddit
            }
            for subreddit in subreddits
        }
        self.log(f'{subreddits}')
        return subreddits

    def get_keywords_dict(self, category, site_name="all"):
        return self.load_no_videos(self.read(self.filenames[self.category]))

    def load_imagedata(self):
        self.page = 1
        filename = os.path.join(self.this_directory, self.json_dir,
                                self.subreddits[self.subreddit]['json'])
        self.log(f'filename: {filename}')
        success = False
        try:
            with open(filename, 'r') as file:
                self.image_data = json.load(file)
            success = True
        except Exception as e:
            self.log(f"Exception noted: {e}")
            self.image_data = {}

        return success

    def log(self, text):
        print(f'log : {text}')
