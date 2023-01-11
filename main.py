from threading import Thread
import customtkinter as ctk
import tkinter as tk
import os


class StartWindow():
    def __init__(self, root):
        self.root = root

        self.frame_main = ctk.CTkFrame(root, fg_color = None)
        self.frame_main.pack(expand = True)

        self.entry_link = ctk.CTkEntry(self.frame_main, justify = 'center', width = 500)
        self.entry_link.pack(side = 'top')

        self.label_WhToDo = ctk.CTkLabel(self.frame_main, text = 'Put your utube link here ↑')
        self.label_WhToDo.pack(side = 'top')


def main():
    root = ctk.CTk()
    root.geometry('900x500')
    root.resizable(False, False)

    root.attributes('-alpha', 0.96)

    StartWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()