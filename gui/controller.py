import subprocess as sp
import time
import os
from shutil import which


def is_tool(name):
    return which(name) is not None


class Controller:

    def run_spider(self):
        self.set_statusbar_text('Scraping pages, please wait...')
        if self.subreddit == 'all':
            for subreddit in self.subreddits:  # All sites except 'all'
                if subreddit != 'all':
                    self.scrape_site(subreddit)
        else:
            self.scrape_site(self.subreddit)
        self.load_imagedata()
        self.set_statusbar_text('Scraping done!')

    def scrape_site(self, subreddit):
        json_name = os.path.join(self.this_directory, self.json_dir)
        self.log(json_name)
        time.sleep(3)
        json_name = os.path.join(json_name, self.subreddits[subreddit]['json'])
        self.log(f'json_name: {json_name}')
        if os.path.isfile(json_name):
            self.log('its a file!\nremoving file {json_name}')
            os.remove(json_name)
        argument = 'subreddit={}'.format(self.subreddits[self.subreddit]['url_key'])
        self.log(argument)
        command_list = ['scrapy', 'crawl',
            'pics', '-o',
            json_name,
            '-a', argument]
        self.log(command_list)
        proc = sp.run(command_list, cwd=self.this_directory)
        self.log("done!")
        self.log(f'proc: {proc}')
        time.sleep(3)
        if hasattr(self, 'dbmgr'):
            try:
                self.dbmgr.load_file(json_name, site, category, keyword_name)
            except Exception as e:
                self.log(f'got exception from load_file: {e}')
        if self.load_imagedata():
            self.update_thumbs()

    def open_image(self, filename):
        self.log(f"Opening: {filename}")
        if is_tool('feh'):
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
