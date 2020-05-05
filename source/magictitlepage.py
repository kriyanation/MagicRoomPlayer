# -*- coding: utf8 -*-
import os
import tkinter as tk
from tkinter import ttk, font, Menu, simpledialog
import Data_Flow
import unicodedata
import vlc, sys, time
import pageutils,subprocess,configparser
from pathlib import Path
from tkinter import messagebox

import PIL
from PIL import Image, ImageTk,ImageFont
_isLinux = sys.platform.startswith('linux')
config = configparser.RawConfigParser()
two_up = Path(__file__).resolve().parents[2]
print(str(two_up)+'/magic.cfg')
config.read(str(two_up)+'/magic.cfg')
imageroot = Data_Flow.imageroot





class MagicTitlePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        s = ttk.Style(self)
        s.configure('Green.TButton', background='dark slate gray', foreground='PeachPuff2')
        s.map('Green.TButton', background=[('active', '!disabled', 'dark olive green'), ('pressed', 'PeachPuff2')],
              foreground=[('pressed', 'PeachPuff2'), ('active', 'PeachPuff2')])

        s.configure('TScrollbar', background='dark slate gray', foreground='dark slate gray')
        s.map('TScrollbar', background=[('active', '!disabled', 'dark olive green'), ('disabled', 'dark slate gray')],
              foreground=[('active', 'PeachPuff2'), ('disabled', 'dark slate gray')])
        self.video_mode = False
        print(type(parent).__name__)
        self.parent_window = parent
        self.pen_color = 'bisque2'
        self.old_x, self.old_y = None, None
        self.configure(background='dark slate gray')
        self.quoteframe = tk.Frame(self)
        self.quoteframe.configure(background='dark slate gray')
        self.quoteframe.pack(fill=tk.X, side=tk.TOP,anchor=tk.CENTER)
        self.quote_text = Data_Flow.get_Quote()
        self.quote_textwidget = tk.Text(self.quoteframe, borderwidth=0,highlightthickness=0,relief=tk.FLAT,wrap=tk.WORD,font= ('TkDefaultFont',12), bd=2,height=2,foreground = 'PeachPuff2',background=
                                     'dark slate gray')
        #self.labelframeone = ttk.Labelframe(self, width=parent.screen_width / 2.0, height=parent.screen_height / 2.0,
        #                                    text="Introduction", relief=tk.RIDGE, style='Red.TLabelframe')
        self.labelframeone = ttk.Labelframe(self,
                                            text="The Ice-Breaker", relief=tk.RIDGE, style='Red.TLabelframe')

        self.counter = 0
        pageutils.animate_text( self.quoteframe, self.quote_text, self.counter,self.quote_textwidget,len(self.quote_text)-1)

        self.quote_textwidget.pack(pady=5,side = tk.TOP,anchor=tk.CENTER)
        self.buttonimage = tk.PhotoImage(file="../images/speaker.png")

        self.quote_audio_button = ttk.Button(self.quoteframe,text="hello", image = self.buttonimage,command=lambda: self.play_quote_audio(self.quote_text),
                                         style='Green.TButton')
        self.quote_audio_button.pack(padx=100,side=tk.TOP)
        self.labelframeone.pack(padx = 80,fill=tk.BOTH,expand=tk.TRUE)
        self.title_intro()

        args = []
        if _isLinux:
            args.append('--no-xlib')
        try:
            self.Instance = vlc.Instance(args)
        except (NameError, OSError, AttributeError) as err:
            print(err)
            print(err.args)

        if(self.Instance != None):
            self.player = self.Instance.media_player_new()
        parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
        parent.update()

    def paint_text(self,event):
        answer = simpledialog.askstring("Text to add", "Add text to the location",
                                        parent=self.parent_window)
        self.canvas.create_text(event.x,event.y,font=("comic sans", 15, "bold"),text=answer,fill=self.pen_color)

    def paint(self, event):

        #x1, y1 = (event.x - 1), (event.y - 1)
        #x2, y2 = (event.x + 1), (event.y + 1)
        #self.canvas.create_oval(x1, y1, x2, y2, fill='white')

        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                               width=5, fill=self.pen_color,
                                               capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y
    def play_video(self):
        try:
         #self.player.play()
         self.list_player.play()
        except (NameError, OSError, AttributeError):
         messagebox.showwarning("Warning", "VLC is unable to play the file: "+self.title_video_str)




    def new_window(self):
        self.player.stop()
        subprocess.Popen(['vlc', '-vvv', self.title_video_str])

    def pause_video(self):
        #self.player.pause()
        self.list_player.pause()
       #self.player.set_fullscreen(False)
    def show_overview_image(self):
        print("Down pressed")
        self.title_intro()

    def show_video_intro(self):
        self.video_mode = True
        self.title_video()
        try:
            self.list_player.play()
        except (NameError, OSError, AttributeError):
            messagebox.showwarning("Warning", "VLC is unable to play the file: " + self.title_video_str)

    def play_quote_audio(self,text):
        pageutils.playtextsound(text)

    def open_image_window(self,title_image):
        #subprocess.run([title_image], check=False)
        if sys.platform == "win32":
            os.startfile(title_image)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, title_image])

    def save_image_window(self):
        # subprocess.run([title_image], check=False)
        self.canvas.postscript(file='title_image'+self.title_text+".eps")
        image = Image.open('title_image'+self.title_text+".eps")
        image.save(Data_Flow.saved_canvas+os.path.sep+"title_image"+self.title_text+'.png','png')
        image.close()
        os.remove('title_image'+self.title_text+".eps")
        messagebox.showinfo("Information","Image saved under saved_images folder")

    def show_popup_menu(self, event):
        self.popup_menu.tk_popup(event.x_root, event.y_root)
        self.popup_menu.entryconfig("Text",command=lambda:self.paint_text(event))

    def title_intro(self):


        self.title_text = Data_Flow.get_Title()



        self.topic_label = ttk.Label(self.labelframeone, text = self.title_text,font= ('TkDefaultFont', 16), foreground = 'PeachPuff2',background = 'dark slate gray', wraplength=self.parent_window.screen_width/2.5)
        self.topic_label.pack(pady=10,anchor = tk.CENTER)

        title_image = Data_Flow.get_title_image()
        self.image_frame = tk.Frame(self.labelframeone)
        self.image_frame.configure(background='dark slate gray')
        self.new_window_image_button = ttk.Button(self.image_frame, text="Zoom Image",
                                                  command=lambda: self.open_image_window(title_image), style='Green.TButton')
        self.image_save_button = ttk.Button(self.image_frame, text="Save Board",
                                                  style='Green.TButton')

        self.show_video_button = ttk.Button(self.image_frame, text="Show Video",
                                            command=self.show_video_intro,
                                            style='Green.TButton')


        self.new_window_image_button.pack(pady=5, side=tk.LEFT)
        self.image_save_button.pack(padx=5, side=tk.LEFT)
        self.show_video_button.pack(pady=5, side=tk.LEFT)
        self.image_frame.pack(anchor=tk.CENTER)
        #self.canvas = tk.Canvas(self.labelframeone,
        #                width=self.parent_window.screen_width/2.0,
        #                height=self.parent_window.screen_height/2.5,background='dark slate gray',borderwidth = 0, highlightthickness=0,relief=tk.FLAT)

        self.canvas = tk.Canvas(self.labelframeone,
                                background='dark slate gray',borderwidth = 0, highlightthickness=0,relief=tk.FLAT)
        self.popup_menu = Menu(self.canvas,background='dark slate gray',foreground='peachpuff2')
        self.popup_menu.add_command(label="Dark",command=self.switch_to_dark)
        self.popup_menu.add_command(label="Light", command=self.switch_to_light)
        self.popup_menu.add_command(label="Text")

        self.canvas.pack( padx=3, pady=20)
        self.canvas.bind('<Button-3>', self.show_popup_menu)
        self.image_save_button.configure(command=self.save_image_window)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.bind("<Configure>", self.resize)
        self.notes_display()
        try:
            self.img = Image.open(title_image)

            device = config.get("section1",'device_type')

           #self.img = self.img.resize((400, 400))
            #self.img1 = ImageTk.PhotoImage(self.img)


        except (FileNotFoundError, IsADirectoryError):
            messagebox.showerror("Error", "Title image not found in the path \n"+title_image)
            self.parent_window.destroy()
            sys.exit()

    def resize(self,event):
        if not self.video_mode:
            self.img = self.img.resize(
                (int(self.winfo_width()/2)-100, int(self.winfo_height()/2)-100), Image.ANTIALIAS)

            self.img1 = ImageTk.PhotoImage(self.img)
            self.canvas.configure(width= int(self.winfo_width()/2),height= int(self.winfo_height()/2))
            self.title_image_id = self.canvas.create_image(10, 10, image=self.img1,
                                                           anchor=tk.NW)


    def title_video(self):
        self.canvas.delete("all")
        self.image_frame.pack_forget()
        self.canvas.pack_forget()
        self.title_video_str = "https://www.youtube.com/watch?v=zab3ePtO7Jc" #Data_Flow.get_title_video()

        self.media = self.Instance.media_new(str(self.title_video_str))  # Path, unicode
        self.media_list = self.Instance.media_list_new([self.title_video_str])
        self.player.set_media(self.media)

        self.list_player = self.Instance.media_list_player_new()
        self.list_player.set_media_player(self.player)
        self.list_player.set_media_list(self.media_list)
        self.canvas.delete(self.title_image_id)




        self.controlframe = tk.Frame(self.labelframeone)
        self.controlframe.configure(background='dark slate gray')
        self.play_button = ttk.Button(self.controlframe, text="Play", command=self.play_video, style='Green.TButton')
        self.pause_button = ttk.Button(self.controlframe, text="Pause", command=self.pause_video,
                                       style='Green.TButton')
        self.new_screen_button = ttk.Button(self.controlframe, text="Zoom Video", command=self.new_window,
                                           style='Green.TButton')


        self.play_button.pack(side=tk.LEFT)
        self.pause_button.pack(side=tk.LEFT,padx=10)
        self.new_screen_button.pack(side=tk.LEFT,padx=10)
        self.controlframe.pack()
        self.canvas.pack(padx=10, fill=tk.BOTH,expand = tk.TRUE,anchor=tk.CENTER)
        self.player_frame_info = self.canvas.winfo_id()  # .winfo_visualid()?
        if(_isLinux):
            self.player.set_xwindow(self.player_frame_info)
        else:
            self.list_player.set_hwnd(self.player_frame_info)
        #self.player.play()
        #self.notes_display()
        self.show_video_button.config(state='disabled')

    def notes_display(self):
        video_notes_info = Data_Flow.get_Running_Notes()
        video_notes = video_notes_info[0]
        self.video_note_text = tk.Text(self, pady=10, borderwidth=0, highlightthickness=0, relief=tk.SUNKEN,
                                       wrap=tk.WORD, font=("comic sans", 15), height=8, foreground="PeachPuff2",
                                       background='dark slate gray')
        pageutils.animate_text(self, video_notes, 0, self.video_note_text, len(video_notes) - 1)
        self.scrollbar = ttk.Scrollbar(self)
        self.video_note_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.video_note_text.yview, style='TScrollbar')
        self.video_note_text.pack(anchor=tk.S)

    def OnConfigure(self, *unused):
        """Some widget configuration changed.
        """
        # <https://www.Tcl.Tk/man/tcl8.6/TkCmd/bind.htm#M12>
        self._geometry = ''  # force .OnResize in .OnTick, recursive?

    def reset(self, event):
        self.old_x, self.old_y = None, None


    def animate_text(self, text, counter,label, counter_max):
        print(text)
        label.config(text=text[:counter])
        if counter > counter_max:
            #self.playtextsound(quote_text)
            return
        self.after(100, lambda: self.animate_text(text,counter + 1,label,counter_max))

    def switch_to_dark(self):
        self.pen_color = 'gray26'

    def switch_to_light(self):
        self.pen_color = 'bisque2'






