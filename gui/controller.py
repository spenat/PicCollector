import subprocess as sp
import random
import time
import os
from shutil import which
from .image_viewer import ImageViewer


def is_tool(name):
    return which(name) is not None


class Controller:

    slide_running = False

    def run_spider(self):
        self.set_statusbar_text('Scraping pages, please wait...')
        if self.subreddit == 'all':
            for subreddit in self.subreddits:
                if subreddit != 'all':
                    self.scrape_site(subreddit)
        else:
            self.scrape_site(self.subreddit)
        self.load_imagedata()
        self.update_thumbs()
        self.load_select_list()
        self.set_statusbar_text('Scraping done!')

    def scrape_site(self, subreddit):
        json_name = os.path.join(self.root_directory, self.json_dir)
        time.sleep(3)
        json_name = os.path.join(json_name, self.subreddits[subreddit]['json'])
        self.log(f'json_name: {json_name}')
        if os.path.isfile(json_name):
            self.log('its a file!\nremoving file {json_name}')
            os.remove(json_name)
        argument = 'subreddit={}'.format(
            self.subreddits[subreddit]['url_key'])
        self.log(argument)
        command_list = [
            'python', '-m', 'scrapy', 'crawl', 'pics', '-o', json_name, '-a', argument
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
                    self.subreddits[subreddit]['json'])
                self.dbmgr.load_scrape_result_file(json_filename, subreddit)
                self.subreddits = self.dbmgr.get_subreddit_dict()
            except Exception as exc:
                self.log(f'got exception from load_file: {exc}')

    def native_viewer_destroyed(self, event):
        self.native_viewer = None

    def start_slideshow(self, event):
        if not self.slide_running:
            self.slide_running = True
            self.run_slideshow()

    def stop_slideshow(self, event):
        self.slide_running = False

    def set_background(self):
        path = self.image_data[self.current_image]['images'][0]['path']
        full_path = os.path.join(self.images_dir, path)
        command_list = [
            'feh', '--no-fehbg', '--bg-fill', full_path
        ]
        self.log(command_list)
        proc = sp.run(command_list, cwd=self.root_directory)

    def run_slideshow(self):
        if self.slide_running:
            self.next_image(0)
            self.native_viewer.viewer_window.after(1500, self.run_slideshow)

    def next_image(self, event):
        self.current_image += 1
        if self.current_image >= len(self.image_data):
            self.current_image = 0
        self.set_current_image()

    def prev_image(self, event):
        self.current_image -= 1
        if self.current_image < 0:
            self.current_image = len(self.image_data) - 1
        self.set_current_image()

    def set_current_image(self):
        image_meta = self.image_data[self.current_image]
        path = image_meta['images'][0]['path']
        full_path = os.path.join(self.images_dir, path)
        self.set_statusbar_text(f'Currently showing: {full_path}')
        self.native_viewer.set_image(full_path)

    def random_subreddit(self, event):
        subreddit = list(self.subreddits)[random.randint(1, len(self.subreddits) - 1)]
        self.subreddit = subreddit
        self.load_imagedata()
        self.load_select_list()
        self.update_thumbs()
        self.next_image(0)

    def open_image(self, filename):
        self.log(f"Opening: {filename}")
        player = self.options['viewer']
        if player == 'native':
            if hasattr(self, 'native_viewer') and self.native_viewer:
                self.native_viewer.set_image(filename)
            else:
                self.native_viewer = ImageViewer(self.root, filename, self.options)
                self.native_viewer.viewer_window.bind('<Destroy>', self.native_viewer_destroyed)
                self.native_viewer.viewer_window.bind('s', self.start_slideshow)
                self.native_viewer.viewer_window.bind('d', self.stop_slideshow)
                self.native_viewer.viewer_window.bind('n', self.next_image)
                self.native_viewer.viewer_window.bind('<space>', self.next_image)
                self.native_viewer.viewer_window.bind('p', self.prev_image)
                self.native_viewer.viewer_window.bind('<BackSpace>', self.prev_image)
                self.native_viewer.viewer_window.bind('r', self.random_subreddit)
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
