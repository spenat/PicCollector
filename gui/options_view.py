import os
import json
import _tkinter
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog


class OptionsView:

    options_file = 'options.json'
    default_options_file = 'default_options.json'
    options_window = None

    def __init__(self, root, root_directory, load_options_callback):
        self.root = root
        self.root_directory = root_directory
        self.load_options_callback = load_options_callback
        self.options_file = os.path.join(self.root_directory, 'config',
                                         self.options_file)
        self.default_options_file = os.path.join(self.root_directory, 'config',
                                                 self.default_options_file)
        try:
            self.options = self.load_options()
        except Exception as exc:
            print(f'load_options caused exception: {exc}')
        try:
            self.setup_view()
        except Exception as exc:
            print(f'setup_view caused exception: {exc}')

    def load_options(self, defaults=False):
        options_file = self.default_options_file if defaults else self.options_file
        with open(options_file) as file:
            options = json.load(file)
        return options

    def restore_defaults(self):
        self.options = self.load_options(True)

    def setup_view(self):
        self.options_window = tk.Toplevel(self.root, width=560, height=200)
        self.frame = tk.Frame(self.options_window)
        self.options_label = tk.Label(self.frame,
                                      text="Options",
                                      font=("DejaVu Sans", "16"))
        self.options_label.grid(row=0, column=1, columnspan=1)
        self.viewer_selector_label = tk.Label(self.frame,
                                              text="Viewer",
                                              anchor=tk.W,
                                              justify=tk.LEFT,
                                              width=20)
        self.viewer_selector_label.grid(row=1, column=0, columnspan=1)
        index = self.options['viewer_alts'].index(self.options['viewer'])
        self.viewer_selector = ttk.Combobox(self.frame,
                                            values=self.options['viewer_alts'],
                                            state=['readonly'],
                                            width=44)
        self.viewer_selector.current(newindex=index)
        self.viewer_selector.grid(row=1, column=1, columnspan=2)
        self.current_storage_label = tk.Label(self.frame,
                                              text=self.options['storage'],
                                              width=40)
        self.current_storage_label.grid(row=2, column=0, columnspan=2)
        self.storage_selector = tk.Button(self.frame,
                                          text="Select folder",
                                          command=self.set_storage_folder,
                                          width=20)
        self.storage_selector.grid(row=2, column=2, columnspan=1)
        self.restore_defaults_button = tk.Button(self.frame,
                                                 text="Restore defaults",
                                                 command=self.restore_defaults,
                                                 width=20)
        self.restore_defaults_button.grid(row=3, column=1, columnspan=1)
        self.save_button = tk.Button(self.frame,
                                     text="Save",
                                     command=self.save,
                                     width=20)
        self.save_button.grid(row=3, column=0, columnspan=1)

        self.close_button = tk.Button(self.frame,
                                      text="Close",
                                      command=self.destroy,
                                      width=20)
        self.close_button.grid(row=3, column=2, columnspan=1)
        self.frame.pack(expand=True)

    def set_viewer(self):
        index = self.viewer_selector.current()
        self.options['viewer'] = self.options['viewer_alts'][index]

    def set_storage_folder(self):
        storage_folder = self.options["storage"]
        if storage_folder == "default":
            storage_folder = os.path.join(self.root_directory, 'pic_collector',
                                          'images')
        storage_folder = filedialog.askdirectory(parent=self.options_window,
                                                 initialdir=storage_folder)
        self.options["storage"] = storage_folder
        self.current_storage_label.configure(text=storage_folder)

    def save(self):
        self.set_viewer()
        try:
            with open(self.options_file, 'w') as file:
                json.dump(self.options, file, indent=4)
        except Exception as exc:
            print(f"Exception caused by {__class__}.save() : {exc}")
        self.load_options_callback()

    def destroy(self):
        self.options_window.destroy()
        self.options_window = None
