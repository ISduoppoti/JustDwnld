from pytube import YouTube, Playlist
from PIL import Image, ImageTk
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

        self.btn_next = ctk.CTkButton(self.root, text = 'Next', fg_color = '#388D70', hover_color = '#307860', command = self.preparing_info)

        #----
        #----

        self.label_loading = ctk.CTkLabel(self.root, text = 'Loading...')

        #----

        self.main_list = [self.frame_main, self.label_WhToDo, self.btn_next, self.label_loading]

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

    def preparing_info(self):
        self.label_loading.pack(side = 'bottom')

        def main():
            self.dwnld_thumbnail()

            if  'www.youtube.com/watch?v=' in self.link:
                self.yt = YouTube(self.link)
                self.selfdestroying()
                Video_dwnlder(self.root, self.link, self.thumbnail, self.yt)

            elif 'www.youtube.com/playlist?list=' in self.link:
                self.yt = Playlist(self.link)
                self.selfdestroying()
                Playlist_dwnlder(self.root, self.link, self.thumbnail, self.yt)

            else:
                self.label_WhToDo.configure(text = 'I dont know this type of link...')

                return False

        Thread(target = main, daemon = True).start()

    def dwnld_thumbnail(self):
        import regex as re
        import requests
        from io import BytesIO

        TEMPLATE_VIDEO = 'https://i.ytimg.com/vi/{}/maxresdefault.jpg'
        TEMPLATE_STREAM = 'https://i.ytimg.com/vi/{}/maxresdefault_live.jpg'
        VARIANT_B = 'https://i.ytimg.com/vi/{}/sddefault.jpg'
        VARIANT_BB = 'https://i.ytimg.com/vi/{}/hqdefault.jpg'

        result = re.search(r'watch\?v=([a-zA-Z0-9_-]*)', self.link)

        if result:
            t_url = None
            video_id = result.groups()[0]

            req = requests.get(self.link)
            page = req.content.decode('utf-8')

            if TEMPLATE_STREAM.format(video_id) in page:
                t_url = TEMPLATE_STREAM.format(video_id)

            elif TEMPLATE_VIDEO.format(video_id) in page:
                t_url = TEMPLATE_VIDEO.format(video_id)
            
            elif VARIANT_B.format(video_id) in page:
                t_url = VARIANT_B.format(video_id)
            
            else:
                t_url = VARIANT_BB.format(video_id)

            self.req = requests.get(t_url)

            pil_image = Image.open(BytesIO(self.req.content))
            pil_image = pil_image.resize((640, 360))
            self.thumbnail = ImageTk.PhotoImage(pil_image)

    def selfdestroying(self):
        for widget in self.main_list:
            widget.pack_forget()



class Video_dwnlder():
    def __init__(self, root, link, thumbnail, yt):
        self.root = root
        self.link = link
        self.thumbnail = thumbnail
        self.yt = yt


        #---

        self.frame_left = ctk.CTkFrame(self.root, fg_color = '#29292E')
        self.frame_left.pack(side = 'left', fill = tk.Y)

        #---
        #----

        self.frame_for_format = ctk.CTkFrame(self.frame_left, fg_color = None)
        self.frame_for_format.pack(side = 'top', fill = tk.X, pady = 5)

        #----
        #-----

        self.b_var = tk.BooleanVar()
        self.b_var.set(1)

        self.radio_mp3 = ctk.CTkRadioButton(self.frame_for_format, text = 'mp3', variable = self.b_var, value = 1, width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_mp3.pack(side = 'left', expand = True)

        self.radio_mp4 = ctk.CTkRadioButton(self.frame_for_format, text = 'mp4', variable = self.b_var, value = 0, width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_mp4.pack(side = 'right', expand = True)

        #-----
        #----

        self.frame_for_res = ctk.CTkFrame(self.frame_left, fg_color = None)
        self.frame_for_res.pack(side = 'top', fill = tk.X, pady = 5)

        #----
        #-----

        self.i_var = tk.IntVar()
        self.i_var.set(2)

        self.radio_360p = ctk.CTkRadioButton(self.frame_for_res, text = '360p', variable = self.i_var, value = 0, width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_360p.pack(side = 'left', padx = 3, expand = True)

        self.radio_480p = ctk.CTkRadioButton(self.frame_for_res, text = '480p', variable = self.i_var, value = 1, width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_480p.pack(side = 'left', padx = 3, expand = True)

        self.radio_720p = ctk.CTkRadioButton(self.frame_for_res, text = '720p', variable = self.i_var, value = 2, width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_720p.pack(side = 'left', padx = 3, expand = True)

        #-----


class Playlist_dwnlder():
    def __init__(self, root, link, thumbnail, yt):
        self.root = root
        self.link = link
        self.thumbnail = thumbnail
        self.yt = yt


def main():
    root = ctk.CTk()
    root.geometry('900x500')
    root.resizable(False, False)

    root.attributes('-alpha', 0.96)

    StartWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()