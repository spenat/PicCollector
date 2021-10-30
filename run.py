import os
import _tkinter
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from gui.pic_collector import PicCollector


root = tk.Tk()

with ThreadPoolExecutor(max_workers=60) as executor:
    piccollector = PicCollector(root, executor,
                                os.path.dirname(os.path.realpath(__file__)))
    root.mainloop()
