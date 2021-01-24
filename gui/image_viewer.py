import os
import json
import _tkinter
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk


class ImageViewer:
    def __init__(self, root, filename, options):
        self.root = root
        self.filename = filename
        self.options = options
        self.window_width = self.options['viewerOptions']['width']
        self.window_height = self.options['viewerOptions']['height']
        try:
            self.setup()
        except Exception as exc:
            print(f'{__class__} got exception : {exc}')

    def create_picture_label(self):
        if hasattr(self, 'picture_label'):
            self.picture_label.grid_remove()
        self.picture_label = tk.Label(self.frame,
                                      width=self.window_width,
                                      height=self.window_height,
                                      bg='#222222')
        self.picture_label.grid(row=0, column=0)

    def set_image(self, filename):
        self.filename = filename
        image = Image.open(self.filename)
        image_width, image_height = image._size
        if image_height > self.window_height:
            scale = self.window_height / image_height
            new_width = int(float(image_width) * scale)
            new_height = int(float(image_height) * scale)
            new_image = Image.open(self.filename).resize((new_width, new_height),
                                                         Image.ANTIALIAS)
        else:
             new_image = Image.open(self.filename)
        render = ImageTk.PhotoImage(new_image)
        self.picture_label.configure(image=render)
        self.picture_label.image = render

    def create_viewer_window(self):
        self.viewer_window = tk.Toplevel(self.root,
                                         width=self.window_width,
                                         height=self.window_height)
        def destroy_viewer_window(event):
            self.viewer_window.destroy()
        self.viewer_window.bind('q', destroy_viewer_window)
        self.frame = tk.Frame(self.viewer_window)

    def setup(self):
        self.create_viewer_window()
        self.create_picture_label()
        self.set_image(self.filename)
        self.frame.pack(expand=True)
