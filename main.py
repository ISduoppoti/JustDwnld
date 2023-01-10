from threading import Thread
import customtkinter as ctk
import tkinter as tk
import os


def main():
    root = ctk.CTk()
    root.geometry('900x500')
    root.resizable(False, False)

    root.attributes('-alpha', 0.96)

    root.mainloop()

if __name__ == '__main__':
    main()