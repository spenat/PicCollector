import os
import _tkinter
import tkinter as tk
import tkinter.ttk as ttk
from  tkinter import filedialog
from PIL import Image, ImageTk
from .options_view import OptionsView


class View:

    thumbs = []
    page_counter = None
    image_data = None
    cards = []
    card_views = {}
    wait_sign = None
    button_row = 5
    options_view = None
    options = None

    def setup_view(self):
        next_button = tk.Button(self.root, text="Next", command=self.next_page, height=3, width=10)
        prev_button = tk.Button(self.root, text="Prev", command=self.prev_page, height=3, width=10)
        
        def scrape():
            self.executor.submit(self.run_spider)

        scrape_button = tk.Button(self.root, text="Get pictures", command=scrape, height=1, width=10)
        scrape_button.grid(row=0, column=2)

        def options():
            self.executor.submit(self.show_options)

        show_options_button = tk.Button(self.root, text="Options", command=options, height=1, width=10)
        show_options_button.grid(row=0, column=4)

        next_button.grid(row=self.button_row,column=3)
        prev_button.grid(row=self.button_row, column=1)

        if self.debug:
            self.create_debug_text()

        self.load_select_list()
        self.setup_page_counter()
        self.setup_statusbar()
        if len(self.image_data) > 0:
            self.update_thumbs()
        else:
            self.empty_subreddit()

        def quit(event):
            self.root.destroy()
        self.root.bind('q', quit)

    def load_select_list(self):
        if hasattr(self, 'subreddit_select') and self.subreddit_select:
            self.subreddit_select.destroy()
        select_list = sorted(list(self.subreddits))
        subreddit_index = select_list.index(self.subreddit) + 1
        first_sub = select_list[0]
        if 'quantity' in self.subreddits[first_sub]:
            select_list = [s + ' (' + str(self.subreddits[s]['quantity']) + ')' for s in select_list]
        select_list = ['Add subreddit'] + select_list
        self.subreddit_select = ttk.Combobox(self.root, values=select_list, state=['readonly'])
        self.subreddit_select.current(newindex=subreddit_index)
        self.subreddit_select.grid(row=0, column=0)
        self.subreddit_select.bind('<<ComboboxSelected>>', self.set_subreddit)

    def empty_subreddit(self):
        if hasattr(self, 'empty_void') and self.empty_void:
            self.empty_void.grid_remove()
        self.set_statusbar_text("This subreddit has not been scraped yet. Press \"Get pictures\" to start scraping")
        empty_void = tk.Frame(self.root, width=5*240, height=4*150)
        empty_void.grid(row=1, column=0, columnspan=5)
        self.empty_void = empty_void
        

    def make_adder(self):
        adder = tk.Toplevel(self.root)
        frame = tk.Frame(adder)
        label = tk.Label(frame, text=f"Add subreddit: ")
        text_box = tk.Entry(frame, width=20)
        frame.pack()
        label.grid(row=0, column=0)
        text_box.grid(row=0, column=1)
        text_box.bind('<Return>', self.add_subreddit)
        self.adder = adder

    def add_subreddit(self, event):
        new_subreddit = event.widget.get()
        self.adder.destroy()
        filename = self.subreddits_filename
        with open(filename, 'a') as fo:
            fo.write(new_subreddit + '\n')
        self.load_model()
        self.load_select_list()
        self.log(f"Added subreddit: {new_subreddit}")

    def create_debug_text(self):
        text_frame = tk.Text(self.root, width=140, height=47)
        self.debug_text = text_frame 
        self.debug_text.grid(row=0, column=5, rowspan=6)

    def setup_statusbar(self):
        statusbar = tk.Label(self.root, text="Status", anchor=tk.W, justify=tk.LEFT, width=120)
        statusbar.grid(row=7, column=0, columnspan=4)
        self.statusbar = statusbar

    def set_statusbar_text(self, new_text):
        self.statusbar.configure(text=new_text)

    def set_subreddit(self, event):
        subreddit = event.widget.get()
        if subreddit == 'Add subreddit':
            self.make_adder()
            return
        subreddit = subreddit.split(' ')[0]
        self.subreddit = subreddit
        self.page = 1

        self.log(f'{self.subreddit}')
        if self.load_imagedata():
            self.update_thumbs()
        else:
            self.empty_subreddit()
            self.remove_thumbs()

    def next_page(self):
        if self.page*20 < len(self.image_data):
            self.page += 1
            self.update_thumbs()

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.update_thumbs()

    def setup_page_counter(self):
        if self.page_counter:
            self.page_counter.grid_remove()
        if not self.image_data:
            return
        total_pages = len(self.image_data) // 20
        if len(self.image_data) % 20 != 0:
            total_pages += 1
        page_text = f' of {total_pages}'
        page_counter = tk.Frame(self.root)
        this_page = tk.Entry(page_counter, width=6)
        this_page.grid(row=0, column=0)
        self.this_page = this_page
        self.this_page.insert(0, self.page)
        self.this_page.bind('<Return>', self.change_page)
        total_page_label = tk.Label(page_counter, text=page_text)
        total_page_label.grid(row=0, column=1)
        page_counter.grid(row=self.button_row, column=2)
        self.page_counter = page_counter

    def change_page(self, event):
        self.log(event)
        self.page = int(event.widget.get())
        self.update_thumbs()

    def remove_thumbs(self):
        if self.thumbs:
            for thumb in self.thumbs:
                thumb.grid_remove()
            self.thumbs = []

    def update_thumbs(self):
        count = 0
        if hasattr(self, 'empty_void') and self.empty_void:
            self.empty_void.grid_remove()
        self.remove_thumbs()
        page = self.page
        tpp = 20 # thumbs per page 20
        tpr = 5 # thumbs per row 5
        if (page * tpp < len(self.image_data)):
            image_data = self.image_data[(page - 1)*tpp:page*tpp]
        elif ((page - 1)*tpp < len(self.image_data)):
            image_data = self.image_data[(page - 1)*tpp:page*tpp]
        else:
            return
        for image_meta in image_data:
            try:
                if len(image_meta['images']) > 0:
                    image_path = image_meta['images'][0]['path']
                    thumb_path = os.path.join('thumbs/small/', image_path.split('/')[-1])
                    img_path = os.path.join(self.root_directory, 'pic_collector/images/', thumb_path)
                    full_image = os.path.join(self.root_directory, 'pic_collector/images/', image_path)
                else:
                    img_path = os.path.join(self.root_directory, 'pic_collector/not-found.gif')
                    if len(image_meta['image_urls']) > 0:
                        full_image = image_meta['image_urls'][0]
                    else:
                        full_image = "Missing url"
            except Exception as exc:
                self.log(f'exception in img_path: {exc}')
            description = image_meta['description']
            try:
                image = Image.open(img_path)
            except Exception as exc:
                self.log(f'exception in img_path: {exc}')
                img_path = os.path.join(self.root_directory, 'pic_collector/not-found.gif')
                image = Image.open(img_path)
            render = ImageTk.PhotoImage(image)
            thumb = tk.Label(self.root, image=render, width=240, height=150, bg='#999999', relief=tk.RAISED)
            thumb.image = render
            def mouseover_():
                fi = full_image
                d = description
                def mouseover(event):
                    status_text = f'Full image: {fi} (Click to open)\nDescription: {d}'
                    self.set_statusbar_text(status_text)
                return mouseover

            def click_():
                fi = full_image
                i = image_meta
                def click(event):
                    self.log(event)
                    def c():
                        self.open_image(fi)
                    thing = self.executor.submit(c)
                    self.log(f'thing : {thing}')
                return click

            self.thumbs += [thumb]
            thumb.grid(row=(count // tpr) + 1, column=(count % tpr))
            thumb.bind('<Button-1>', click_())
            thumb.bind('<Enter>', mouseover_())
            count += 1
        
        self.setup_page_counter()

    def show_options(self):
        if not self.options_view:
            options_view = OptionsView(self.root, self.root_directory, self.load_options)
            self.options_view = options_view
        elif not self.options_view.options_window:
            self.options_view.setup_view()

    def log(self, log_str):
        if self.debug:
            print(f'{self.__class__} : {log_str}')
        if hasattr(self, 'debug_text'):
            self.debug_text.insert('@0,0', f'{log_str}\n')
