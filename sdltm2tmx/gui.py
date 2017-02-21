import os
import tkinter as tk
from tkinter import filedialog, StringVar

import sys
# from sdltm2tmx import run as run_sdltm2tmx


class Application(tk.Frame):
    """
    main window
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.sdltm_path = StringVar()
        self.USERHOME = os.getenv('HOME')
        self.tmx_tar_path = StringVar()
        print(sys.path)

    def create_widgets(self):
        self.get_sdltm_path_button = tk.Button(self, fg='white', bg='black')
        self.get_sdltm_path_button['text'] = 'choose sdltm_path'
        self.get_sdltm_path_button['command'] = self.get_sdltm_path
        self.get_sdltm_path_button.pack(side='top',
                                        expand=0,
                                        padx=12,
                                        pady=12)

        self.sdltm_path_label = tk.Label(self)
        self.sdltm_path_label['text'] = 'sdltm path'
        self.sdltm_path_label.pack(side='top',
                                   expand=1,
                                   padx=12,
                                   pady=12)

        self.get_tmx_target_dir_button = tk.Button(self, fg='white', bg='black')
        self.get_tmx_target_dir_button['text'] = 'choose tmx target directory'
        self.get_tmx_target_dir_button['command'] = self.get_tmx_target_dir
        self.get_tmx_target_dir_button.pack(side='top',
                                            expand=0,
                                            padx=12,
                                            pady=12)

        self.tmx_path_label = tk.Label(self)
        self.tmx_path_label['text'] = 'tmx target directory'
        self.tmx_path_label.pack(side='top',
                                 expand=1,
                                 padx=12,
                                 pady=12)

        self.run_convert = tk.Button(self,
                                     text='convert sdltm',
                                     command=self.run_sdltm_convert)
        self.run_convert.pack(side='bottom')

        self.quit = tk.Button(self,
                              text='Quit',
                              fg='red',
                              command=root.destroy)
        self.quit.pack(side='bottom')

    def get_sdltm_path(self):
        initial_dir = self.USERHOME
        initial_dir = '/home/lemur/python/sdltm2tmx/sdltm2tmx'
        sdltm_path = filedialog.askopenfilename(initialdir=initial_dir,
                                                filetypes=[('sdltm', '.sdltm')],
                                                title='sdltm path')
        self.sdltm_path.set(sdltm_path)
        self.sdltm_path_label['text'] = self.sdltm_path.get()

    def get_tmx_target_dir(self):
        initial_dir = self.USERHOME
        tmx_target_dir = filedialog.askdirectory(initialdir=initial_dir)
        self.tmx_tar_path.set(tmx_target_dir)
        self.tmx_path_label['text'] = self.tmx_tar_path.get()


    def run_sdltm_convert(self):
        sdltm_path = self.sdltm_path.get()
        tmx_tar_dir = self.tmx_tar_path.get()
        # run_sdltm2tmx(sdltm_path, tmx_tar_dir)


root = tk.Tk()
app = Application(master=root)
app.master.title('sdltm2tmx')
app.mainloop()
