import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import glob
from functools import partial
from tkinter.constants import W


# make sure you escape spaces on your relevant system
ravenpath = "C:\\Program^ Files\\Raven\\Raven.exe"
valid_extensions = [".mp3", ".wav", ".iff"]

class SoundEditor:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.curr_dir = os.getcwd()
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        file_dialog_button = tk.Button(
            self.window, text="select folder", command=self.get_folder)
        file_dialog_button.grid(row=1, column=1)
        tk.Button(self.window, text="open selected files in raven", command=self.open_selected_files).grid(row=1, column=2)
        tk.Button(self.window, text="reset selected files", command=self.reset_colors).grid(row=2, column=2)
        self.list_files()

    def list_files(self):
        if(hasattr(self, "file_container")):
            self.file_container.destroy()

        file_container = ttk.Frame(self.window)
        tk.Label(file_container, text="file list: ").pack()
        canvas = tk.Canvas(file_container)
        scrollbar = ttk.Scrollbar(
            file_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        file_list = os.listdir(self.curr_dir)
        for filename in file_list:
            if(any(ext in filename for ext in valid_extensions)):
                # it's hard to pass callback functions with arguments so i need to make this hack
                display_with_file_arg = partial(
                    self.display_sound_file, filename)
                tk.Button(scrollable_frame, text=filename,
                          command=display_with_file_arg, width=30).pack()

        file_container.grid(row=2, column=1)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.file_container = file_container
        self.scrollable_frame = scrollable_frame

    def get_folder(self):
        self.curr_dir = filedialog.askdirectory()
        self.list_files()

    def display_sound_file(self, filename):
        self.color_buttons(filename)
        # os.system(ravenpath + self.curr_dir + "/" + filename + " " + self.curr_dir + "/" + "Cricket 17.mp3")

    def color_buttons(self, filename):
        for button in self.scrollable_frame.winfo_children():
           if(button["text"] == filename):
               button["bg"] = "orange"
    
    def open_selected_files(self):
        file_list = ""
        for button in self.scrollable_frame.winfo_children():
           if(button["bg"] == "orange"):
               file_list += self.curr_dir + "/" + button["text"] + " "
        file_list = ravenpath + " " + file_list
        os.system(file_list)

    def reset_colors(self): 
        for button in self.scrollable_frame.winfo_children():
            button["bg"] = "SystemButtonFace"

editor = SoundEditor()
