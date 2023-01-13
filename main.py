from tkinter.filedialog import askdirectory
from pytube import YouTube, Playlist
from PIL import Image, ImageTk
from threading import Thread
import customtkinter as ctk
from pathlib import Path
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
            global Main_window, AltruistInnited

            AltruistInnited = Altruist()

            self.dwnld_thumbnail()

            if  'www.youtube.com/watch?v=' in self.link:
                self.yt = YouTube(self.link)
                self.selfdestroying()
                Main_window = Video_dwnlder(self.root, self.link, self.thumbnail, self.yt, self.req)

            elif 'www.youtube.com/playlist?list=' in self.link:
                self.yt = Playlist(self.link)
                self.selfdestroying()
                Main_window = Playlist_dwnlder(self.root, self.link, self.thumbnail, self.yt, self.req)

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
    def __init__(self, root, link, thumbnail, yt, thumbnail_req):
        self.root = root
        self.link = link
        self.thumbnail = thumbnail
        self.yt = yt
        self.thumbnail_req = thumbnail_req


        #---

        self.frame_left = ctk.CTkFrame(self.root, fg_color = '#29292E', width = 200)
        self.frame_left.pack(side = 'left', fill = tk.Y)

        #---
        #----

        self.frame_settings = ctk.CTkFrame(self.frame_left, fg_color = None)
        self.frame_settings.pack(pady = (20, 10))

        #----
        #-----

        self.frame_for_format = ctk.CTkFrame(self.frame_settings, fg_color = None)
        self.frame_for_format.pack(side = 'top', fill = tk.X, pady = 5)

        #-----
        #------

        self.b_var = tk.BooleanVar()
        self.b_var.set(1)

        self.radio_mp3 = ctk.CTkRadioButton(self.frame_for_format, text = 'mp3', variable = self.b_var, value = 1, width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_mp3.pack(side = 'left', expand = True)

        self.radio_mp4 = ctk.CTkRadioButton(self.frame_for_format, text = 'mp4', variable = self.b_var, value = 0, width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_mp4.pack(side = 'right', expand = True)

        #------
        #-----

        self.frame_for_res = ctk.CTkFrame(self.frame_settings, fg_color = None)
        self.frame_for_res.pack(side = 'top', fill = tk.X, pady = 5)

        #-----
        #------

        self.s_var = tk.StringVar()
        self.s_var.set('720p')

        self.radio_360p = ctk.CTkRadioButton(self.frame_for_res, text = '360p', variable = self.s_var, value = '360p', width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_360p.pack(side = 'left', padx = 3, expand = True)

        self.radio_480p = ctk.CTkRadioButton(self.frame_for_res, text = '480p', variable = self.s_var, value = '480p', width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_480p.pack(side = 'left', padx = 3, expand = True)

        self.radio_720p = ctk.CTkRadioButton(self.frame_for_res, text = '720p', variable = self.s_var, value = '720p', width = 15, height = 15, 
            border_width_checked = 2, border_width_unchecked = 2, fg_color = '#388D70', hover_color = '#307860')
        self.radio_720p.pack(side = 'left', padx = 3, expand = True)

        #------
        #----

        self.frame_for_cutting = ctk.CTkFrame(self.frame_left, fg_color = '#565B5E')
        self.frame_for_cutting.pack(side = 'top')

        #----
        #-----

        self.label_cutfrom = ctk.CTkLabel(self.frame_for_cutting, text = 'Cut from:')
        self.label_cutfrom.pack(side = 'top', pady = 5)

        self.entry_time_cutfrom = ctk.CTkEntry(self.frame_for_cutting, width = 200, justify = tk.CENTER)
        self.entry_time_cutfrom.pack(side = 'top', pady = 5)
        self.entry_time_cutfrom.insert(tk.END, '00:00:00')

        self.label_cutto = ctk.CTkLabel(self.frame_for_cutting, text = 'Cut to:')
        self.label_cutto.pack(side = 'top', pady = 5)

        self.entry_time_cutto = ctk.CTkEntry(self.frame_for_cutting, width = 200, justify = tk.CENTER)
        self.entry_time_cutto.pack(side = 'top', pady = 5)
        self.entry_time_cutto.insert(tk.END, self.get_video_length())

        #-----
        #----

        self.btn_dwnld_th = ctk.CTkButton(self.frame_left, text = 'Dwnld thumbnail', fg_color = '#388D70', hover_color = '#307860', command = self.dwnld_th)
        self.btn_dwnld_th.pack(side = 'bottom', pady = (10, 20))


        #---

        self.frame_right = ctk.CTkFrame(self.root, fg_color = '#1E1E1E')
        self.frame_right.pack(expand = True,  fill = tk.BOTH)

        #---
        #----

        self.frame_th = ctk.CTkFrame(self.frame_right, fg_color = None)
        self.frame_th.pack(expand = True)

        #----
        #-----

        self.label_yt_name = ctk.CTkLabel(self.frame_th, text = self.yt.title, wraplength = 600)
        self.label_yt_name.pack(side = 'top')

        self.label_image = ctk.CTkLabel(self.frame_th, image = self.thumbnail)
        self.label_image.pack()

        #-----
        #----

        self.frame_btn_dwnld = ctk.CTkFrame(self.frame_right, fg_color = None)
        self.frame_btn_dwnld.pack(side = 'bottom', pady = 20, fill = tk.X)

        #----
        #-----

        self.btn_dwnld = ctk.CTkButton(self.frame_btn_dwnld, text = 'Download', fg_color = '#388D70', hover_color = '#307860', command = self.prepare_dwnlding)
        self.btn_dwnld.pack()

        #-----


    def get_video_length(self):
        hours = self.yt.length / 3600
        hours = int(hours)

        minutes = self.yt.length / 60 - hours*60
        minutes = int(minutes)

        seconds = self.yt.length - hours*3600 - minutes*60

        if hours in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            hours = '0'+str(hours)
        else:
            hours = str(hours)

        if minutes in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            minutes = '0'+str(minutes)
        else:
            minutes = str(minutes)

        if seconds in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            seconds = '0'+str(seconds)
        else:
            seconds = str(seconds)

        self.video_length = hours + ':' + minutes + ':' + seconds

        return self.video_length


    def dwnld_th(self):
        output_path = askdirectory()

        if output_path == '':
            output_path = str(Path.home() / "Downloads")

        with open(output_path + '/' + AltruistInnited.get_cure(name= self.yt.title)  + '.png', 'wb') as f:
            f.write(self.thumbnail_req.content)
        self.btn_dwnld_th.configure(text = '_Thumbnail dwnlded_')

    
    def prepare_dwnlding(self):
        output_path = askdirectory()

        if output_path == '':
            output_path = str(Path.home() / "Downloads")

        #If it mp4
        if self.b_var.get() == 0:
            #If we dont need to cut
            if self.entry_time_cutfrom.get() == '00:00:00' and self.entry_time_cutto.get() == self.video_length:
                AltruistInnited.dwnld_video_mp4(yt= self.yt, res= self.s_var.get(), output_path= output_path)

            #If we need to cut
            elif self.entry_time_cutfrom.get() != '00:00:00' or self.entry_time_cutto.get() != self.video_length:
                AltruistInnited.dwnld_video_mp4_cut(yt= self.yt, res= self.s_var.get(), output_path= output_path, cutfrom= self.entry_time_cutfrom.get(), cutto= self.entry_time_cutto.get())


        #If it mp3
        elif self.b_var.get() == 1:
            #If we dont need to cut
            if self.entry_time_cutfrom.get() == '00:00:00' and self.entry_time_cutto.get() == self.video_length:
                AltruistInnited.dwnld_video_mp3(yt= self.yt, output_path= output_path)

            #If we need to cut
            elif self.entry_time_cutfrom.get() != '00:00:00' or self.entry_time_cutto.get() != self.video_length:
                AltruistInnited.dwnld_video_mp3_cut(yt= self.yt, output_path= output_path, cutfrom= self.entry_time_cutfrom.get(), cutto= self.entry_time_cutto.get())



class Playlist_dwnlder():
    def __init__(self, root, link, thumbnail, yt, thumbnail_req):
        self.root = root
        self.link = link
        self.thumbnail = thumbnail
        self.yt = yt
        self.thumbnail_req = thumbnail_req


class Altruist():
    def __init__(self):
        None

    def get_cure(self, name):
        list_of_prohibited = ['/', ':', '*', '?', '"', '<', '>', '|', '.', ',']

        for sign in list_of_prohibited:
            if sign in name:
                name = name.replace(sign, '')

            else:
                None

        if name.find('\\') != -1:
            name = name.replace('\\', '')
        
        self.name = name

        return self.name

    def dwnld_video_mp3(self, yt, output_path):
        def main():
            Main_window.btn_dwnld.configure(text = 'Downloading...')

            video = yt.streams.filter(only_audio = True).first()
            out_file = video.download(output_path = output_path)

            os.rename(out_file, out_file[:-3]+"mp3")

            Main_window.btn_dwnld.configure(text = '_Downloaded_')

        Thread(target = main, daemon = True).start()

    
    def dwnld_video_mp3_cut(self, yt, output_path, cutfrom, cutto):
        def main():
            Main_window.btn_dwnld.configure(text = 'Downloading...')

            current_dir = os.getcwd()

            video = yt.streams.filter(only_audio = True).first()
            out_file = video.download(output_path = output_path)
            new_file = out_file[:-3]+"mp3"

            os.rename(out_file, new_file)

            Main_window.btn_dwnld.configure(text = 'Processing...')

            os.chdir(output_path)

            cmd = 'ffmpeg -i "{}" -ss {} -to {} -async 1 "{}"'.format(new_file, cutfrom,
                cutto, new_file[:-4] + 'C' + '.mp3')

            os.system(cmd)

            os.remove(new_file)

            os.chdir(current_dir)

            Main_window.btn_dwnld.configure(text = '_Downloaded_')

        Thread(target = main, daemon = True).start()

    
    def dwnld_video_mp4(self, yt, res, output_path):
        def main():
            Main_window.btn_dwnld.configure(text = 'Downloading...')

            video = yt.streams.filter(file_extension = 'mp4', res = res).first()
            out_file = video.download(output_path = output_path)

            Main_window.btn_dwnld.configure(text = '_Downloaded_')
        
        Thread(target = main, daemon = True).start()

    
    def dwnld_video_mp4_cut(self, yt, res, output_path, cutfrom, cutto):
        def main():
            Main_window.btn_dwnld.configure(text = 'Downloading...')

            current_dir = os.getcwd()

            video = yt.streams.filter(file_extension = 'mp4', res = res).first()
            out_file = video.download(output_path = output_path)
            full_file = out_file[:-4] + '(full).mp4'

            os.rename(out_file, full_file)

            os.chdir(output_path)

            cmd = 'ffmpeg -i "{}" -ss {} -to {} -async 1 "{}"'.format(full_file, cutfrom,
                cutto, out_file[:-4] + '(cutted)' + '.mp4')

            Main_window.btn_dwnld.configure(text = 'Processing...')

            os.system(cmd)

            os.chdir(current_dir)

            Main_window.btn_dwnld.configure(text = '_Downloaded_')

        Thread(target = main, daemon = True).start()



def main():
    root = ctk.CTk()
    root.geometry('900x500')
    root.resizable(False, False)

    root.attributes('-alpha', 0.96)

    StartWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()