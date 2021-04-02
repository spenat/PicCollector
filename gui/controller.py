import logging
import os
import random
import subprocess as sp
import time
import traceback
from shutil import which

from .image_viewer import ImageViewer


class Controller:

    slide_running = False

    def __init__(self, model, root):
        self.logger = logging.getLogger(f'{__name__} {self.__class__}')
        self.model = model
        self.root = root

    def run_spider(self):
        self.view.set_statusbar_text('Scraping pages, please wait...')
        if self.model.subreddit == 'all':
            for subreddit in self.model.subreddits:
                if subreddit != 'all':
                    self.scrape_site(subreddit)
        else:
            self.scrape_site(self.model.subreddit)
        self.model.load_imagedata()
        self.view.update_thumbs()
        self.view.load_select_list()
        self.view.set_statusbar_text('Scraping done!')

    def scrape_site(self, subreddit):
        json_name = os.path.join(self.model.root_directory, self.model.json_dir)
        time.sleep(3)
        json_name = os.path.join(json_name, self.model.subreddits[subreddit]['json'])
        self.log(f'json_name: {json_name}')
        if os.path.isfile(json_name):
            self.log('its a file!\nremoving file {json_name}')
            os.remove(json_name)
        argument = 'subreddit={}'.format(
            self.model.subreddits[subreddit]['url_key'])
        self.log(argument)
        command_list = [
            'python', '-m', 'scrapy', 'crawl', 'pics', '-o', json_name, '-a', argument
        ]
        self.log(command_list)
        proc = sp.run(command_list, cwd=self.model.root_directory)
        self.log("done!")
        self.log(f'proc: {proc}')
        time.sleep(3)
        if hasattr(self.model, 'dbmgr'):
            try:
                json_filename = os.path.join(
                    self.model.root_directory, self.model.json_dir,
                    self.model.subreddits[subreddit]['json'])
                self.model.dbmgr.load_scrape_result_file(json_filename, subreddit)
                self.model.subreddits = self.model.dbmgr.get_subreddit_dict()
            except Exception as exc:
                self.log(f'got exception from load_file: {json_filename} : {exc}')
                self.log(traceback.format_exc())

    def native_viewer_destroyed(self, event):
        self.native_viewer = None

    def start_slideshow(self, event):
        if not self.slide_running:
            self.slide_running = True
            self.run_slideshow()

    def stop_slideshow(self, event):
        self.slide_running = False

    def set_background(self):
        print(f'self: {self}')
        path = self.model.image_data[self.view.current_image]['images'][0]['path']
        print(f'path: {path}')
        full_path = os.path.join(self.model.images_dir, path)
        command_list = [
            'feh', '--no-fehbg', '--bg-fill', full_path
        ]
        self.log(command_list)
        proc = sp.run(command_list, cwd=self.model.root_directory)
        self.log(proc)

    def run_slideshow(self):
        if self.slide_running:
            self.next_image(0)
            self.native_viewer.viewer_window.after(1500, self.run_slideshow)

    def next_image(self, event):
        self.view.current_image += 1
        if self.view.current_image >= len(self.model.image_data):
            self.view.current_image = 0
        self.set_current_image()

    def prev_image(self, event):
        self.view.current_image -= 1
        if self.view.current_image < 0:
            self.view.current_image = len(self.model.image_data) - 1
        self.set_current_image()

    def set_current_image(self):
        image_meta = self.model.image_data[self.view.current_image]
        path = image_meta['images'][0]['path']
        full_path = os.path.join(self.model.images_dir, path)
        self.view.set_statusbar_text(f'Currently showing: {full_path}')
        self.native_viewer.set_image(full_path)

    def random_subreddit(self, event):
        subreddit = list(self.model.subreddits)[random.randint(1, len(self.model.subreddits) - 1)]
        self.model.subreddit = subreddit
        self.model.load_imagedata()
        self.view.load_select_list()
        self.view.update_thumbs()
        self.next_image(0)

    def set_view(self, view):
        self.view = view

    def open_image(self, filename):
        self.log(f"Opening: {filename}")
        player = self.model.options['viewer']
        self.log(player)
        if player == 'native':
            if hasattr(self, 'native_viewer') and self.native_viewer:
                self.native_viewer.set_image(filename)
            else:
                self.native_viewer = ImageViewer(self.root, filename, self.model.options)
                self.native_viewer.viewer_window.bind('<Destroy>', self.native_viewer_destroyed)
                self.native_viewer.viewer_window.bind('s', self.start_slideshow)
                self.native_viewer.viewer_window.bind('d', self.stop_slideshow)
                self.native_viewer.viewer_window.bind('n', self.next_image)
                self.native_viewer.viewer_window.bind('<space>', self.next_image)
                self.native_viewer.viewer_window.bind('p', self.prev_image)
                self.native_viewer.viewer_window.bind('<BackSpace>', self.prev_image)
                self.native_viewer.viewer_window.bind('r', self.random_subreddit)
            return
        elif which(player):
            pass
        elif which('feh'):
            player = 'feh'
        elif which('gqview'):
            player = 'gqview'
        else:
            player = 'xdg-open'
        if os.path.isfile(filename):
            command_list = [player, filename]
        else:
            self.log('No file')
            return

        proc = sp.Popen(command_list)

    def log(self, text):
        self.logger.info(text)
