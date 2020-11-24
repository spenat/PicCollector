import os
import _tkinter
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from gui.controller import PCController as Controller
from gui.view import PCView as View
from gui.model import PCModel as Model


class PicCollector(Model, View, Controller):
    def __init__(self, root, executor, this_directory):
        self.this_directory = this_directory
        self.root = root
        self.executor = executor
        self.load_model()
        self.load_imagedata()
        self.setup_view()


root = tk.Tk()

with ThreadPoolExecutor(max_workers=60) as executor:
    piccollector = PicCollector(root, executor,
                                os.path.dirname(os.path.realpath(__file__)))
    root.mainloop()
