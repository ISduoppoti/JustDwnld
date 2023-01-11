from threading import Thread
import customtkinter as ctk
import tkinter as tk
import os


class StartWindow():
    def __init__(self, root):
        self.root = root

        #---
        self.frame_main = ctk.CTkFrame(root, fg_color = None)
        self.frame_main.pack(expand = True)
        #---
        #----

        self.entry_link = ctk.CTkEntry(self.frame_main, justify = 'center', width = 500)
        self.entry_link.pack(side = 'top')

        self.entry_link.var = tk.StringVar()
        self.entry_link.configure(textvariable = self.entry_link.var)
        self.entry_link.var.trace_add('write', self.observer_for_entry)

        #----
        #----

        self.label_WhToDo = ctk.CTkLabel(self.frame_main, text = 'Put your utube link here ↑')
        self.label_WhToDo.pack(side = 'top')

        #----

    def observer_for_entry(self, *_):
        self.link = self.entry_link.get()
        if 'www.youtube.com/watch?v=' in self.link or 'www.youtube.com/playlist?list=' in self.link:
            self.entry_link.configure(fg = '#3B927E')
            self.entry_link.fg = 'green'

        elif 'youtu.be/' in self.entry_link.get():
            self.entry_link.configure(fg = '#3B927E')
            self.entry_link.fg = 'green'
            self.link = 'https://www.youtube.com/watch?v=' + self.link[-11:]

        else:
            self.entry_link.configure(fg = '#923B3B')


def main():
    root = ctk.CTk()
    root.geometry('900x500')
    root.resizable(False, False)

    root.attributes('-alpha', 0.96)

    StartWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()