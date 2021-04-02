import os
from pathlib import Path
import _tkinter
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from gui.controller import Controller
from gui.view import View
from db import utils


# if utils.database_exist(os.path.dirname(os.path.realpath(__file__))):
from db.gui_model import Model
# else:
# from gui.model import Model

root_directory = Path(__file__).parent.parent


class PicCollector:

    # controller = Controller()
    # model = Model()
    # view = View()

    def __init__(self, root, executor, root_directory):
        self.root_directory = root_directory
        self.model = Model(root_directory)
        self.controller = Controller(self.model, root)
        self.view = View(root, self.model, executor, self.controller)
        super(PicCollector, self).__init__()
        self.model.load_model()
        self.model.load_imagedata()
        self.view.setup_view()

def run():
    root = tk.Tk()

    with ThreadPoolExecutor(max_workers=60) as executor:
        print(f'root_directory: {root_directory}')
        piccollector = PicCollector(root, executor,
                                    root_directory)
        root.mainloop()
