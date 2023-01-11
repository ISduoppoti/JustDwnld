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
        #----

        self.btn_next = ctk.CTkButton(self.root, text = 'Next', fg_color = '#388D70', hover_color = '#307860', command = )

        #----


    def observer_for_entry(self, *_):
        self.link = self.entry_link.get()
        if 'www.youtube.com/watch?v=' in self.link and len(self.link) == 43 or 'www.youtube.com/playlist?list=' in self.link and len(self.link) == 49:
            self.entry_link.configure(fg = '#3B927E')

            self.btn_next.pack(side = 'bottom')

        elif 'youtu.be/' in self.entry_link.get():
            self.entry_link.configure(fg = '#3B927E')
            self.link = 'https://www.youtube.com/watch?v=' + self.link[-11:]

            self.btn_next.pack(side = 'bottom')

        else:
            self.entry_link.configure(fg = '#923B3B')

            self.label_WhToDo.configure(text = 'Check your link. It must start w https://')




def main():
    root = ctk.CTk()
    root.geometry('900x500')
    root.resizable(False, False)

    root.attributes('-alpha', 0.96)

    StartWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()