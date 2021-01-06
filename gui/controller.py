import subprocess as sp
import time
import os
from shutil import which
from .image_viewer import ImageViewer


def is_tool(name):
    return which(name) is not None


class Controller:
    def run_spider(self):
        self.set_statusbar_text('Scraping pages, please wait...')
        if self.subreddit == 'all':
            for subreddit in self.subreddits:
                if subreddit != 'all':
                    self.scrape_site(subreddit)
        else:
            self.scrape_site(self.subreddit)
        self.load_imagedata()
        self.set_statusbar_text('Scraping done!')

    def scrape_site(self, subreddit):
        json_name = os.path.join(self.root_directory, self.json_dir)
        self.log(json_name)
        time.sleep(3)
        json_name = os.path.join(json_name, self.subreddits[subreddit]['json'])
        self.log(f'json_name: {json_name}')
        if os.path.isfile(json_name):
            self.log('its a file!\nremoving file {json_name}')
            os.remove(json_name)
        argument = 'subreddit={}'.format(
            self.subreddits[self.subreddit]['url_key'])
        self.log(argument)
        command_list = [
            'scrapy', 'crawl', 'pics', '-o', json_name, '-a', argument
        ]
        self.log(command_list)
        proc = sp.run(command_list, cwd=self.root_directory)
        self.log("done!")
        self.log(f'proc: {proc}')
        time.sleep(3)
        if hasattr(self, 'dbmgr'):
            try:
                json_filename = os.path.join(
                    self.root_directory, self.json_dir,
                    self.subreddits[self.subreddit]['json'])
                self.dbmgr.load_file(json_filename, self.subreddit)
                self.subreddits = self.dbmgr.get_subreddit_dict()
                self.load_select_list()
            except Exception as exc:
                self.log(f'got exception from load_file: {exc}')
        if self.load_imagedata():
            self.update_thumbs()

    def native_viewer_destroyed(self, event):
        self.native_viewer = None

    def open_image(self, filename):
        self.log(f"Opening: {filename}")
        player = self.options['viewer']
        if player == 'native':
            if hasattr(self, 'native_viewer') and self.native_viewer:
                self.native_viewer.set_image(filename)
            else:
                self.native_viewer = ImageViewer(self.root, filename, self.options)
                self.native_viewer.viewer_window.bind('<Destroy>', self.native_viewer_destroyed)
            return
        elif is_tool(player):
            pass
        elif is_tool('feh'):
            player = 'feh'
        elif is_tool('gqview'):
            player = 'gqview'
        else:
            player = 'xdg-open'
        if os.path.isfile(filename):
            command_list = [player, filename]
        else:
            self.log('No file')
            return

        proc = sp.Popen(command_list)
