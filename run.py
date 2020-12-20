import os
import _tkinter
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from gui.controller import Controller
from gui.view import View
from db import utils


if utils.database_exist():
    from db.gui_model import Model
else:
    from gui.model import Model

class PicCollector(Model, View, Controller):
    def __init__(self, root, executor, root_directory):
        self.root_directory = root_directory
        self.root = root
        self.executor = executor
        super(PicCollector, self).__init__()
        self.load_model()
        self.load_imagedata()
        self.setup_view()


root = tk.Tk()

with ThreadPoolExecutor(max_workers=60) as executor:
    piccollector = PicCollector(root, executor,
                                os.path.dirname(os.path.realpath(__file__)))
    root.mainloop()
