import tkinter as tk
from tkinter import ttk

import configparser
import subprocess
import sys


import Data_Flow_Player
import pageutils

_isLinux = sys.platform.startswith('linux')

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'

config = configparser.RawConfigParser()
config.read('magic.cfg')

class MagicApplicationVideo(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.configure(background='dark slate gray')
        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background='dark slate gray')
        s.configure('Red.TLabelframe.Label', font=('courier', 12, 'bold', 'italic'))
        s.configure('Red.TLabelframe.Label', foreground='PeachPuff2')
        s.configure('Red.TLabelframe.Label', background='dark slate gray')

        s.configure('Green.TButton', background='dark slate gray', foreground='PeachPuff2')
        s.configure('Horizontal.Green.TScale', background='dark slate gray', foreground='PeachPuff2')
        s.map('Green.TButton', background=[('active', '!disabled', 'dark olive green'), ('pressed', 'PeachPuff2')],
              foreground=[('pressed', 'PeachPuff2'), ('active', 'PeachPuff2')])
        self.application_video_info = Data_Flow_Player.get_application_video()
        self.video_link = self.application_video_info[0]
        self.video_notes = self.application_video_info[1]



        self.labelframeone = ttk.Labelframe(self, width = parent.screen_width/1.8, height = parent.screen_height/2.5, text="Insightful Video", relief=tk.RAISED,style='Red.TLabelframe')
        self.labelframetwo = ttk.Labelframe(self, width = parent.screen_width/1.8, height = parent.screen_height/2.7,text="Things to Note", relief=tk.RIDGE,style= 'Red.TLabelframe')
        self.play_button = ttk.Button(self.labelframeone, text="Play", command= self.play_video,style='Green.TButton')
        self.pause_button = ttk.Button(self.labelframeone, text="Pause", command= self.pause_video,style='Green.TButton')
        self.new_screen_button = ttk.Button(self.labelframeone, text="New Window", command=self.new_window,style='Green.TButton')
        self.video_frame = tk.Frame(self.labelframeone, width = parent.screen_width/2.2, height= parent.screen_height/3.2,background='dark slate gray')

        self.play_button.grid(row=0,column=0)
        self.pause_button.grid(row=0,column=1)
        self.new_screen_button.grid(row=0, column=2)
        self.video_frame.grid(row=1,columnspan = 3,padx=10)
        self.labelframeone.grid_propagate(False)
        self.labelframetwo.grid_propagate(False)
        self.labelframeone.grid(row=0, pady=0, padx = 20)
        self.labelframetwo.grid(row=1, pady= 15, padx = 20)

        args = []
        if _isLinux:
            args.append('--no-xlib')
        # self.Instance = vlc.Instance(args)
        # self.player = self.Instance.media_player_new()

        parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
        parent.update()

        self.fill_video_frame()
        self.fill_notes_frame(parent.screen_width)


    def play_video(self):
       #  self.player.play()
        pass




    def new_window(self):
       # self.player.stop()
        subprocess.Popen(['vlc', '-vvv', self.video_link])

    def pause_video(self):
       # self.player.pause()
       #self.player.set_fullscreen(False)
        pass

    def OnConfigure(self, *unused):
        """Some widget configuration changed.
        """
        # <https://www.Tcl.Tk/man/tcl8.6/TkCmd/bind.htm#M12>
        self._geometry = ''  # force .OnResize in .OnTick, recursive?


    def fill_video_frame(self):
        self.media = self.Instance.media_new(str(self.video_link))  # Path, unicode
        self.player.set_media(self.media)
        player_frame_info = self.video_frame.winfo_id()  # .winfo_visualid()?
        if (_isLinux):
            self.player.set_xwindow(player_frame_info)
        else:
            self.player.set_hwnd(player_frame_info)
       # self.player.play()

    def fill_notes_frame(self,width):
        self.buttonimage = tk.PhotoImage(file="../images/speaker.png")

        self.notes_button = ttk.Button(self.labelframetwo, image=self.buttonimage, command = lambda:pageutils.playtextsound(self.video_notes,'f','tamil'),style='Green.TButton')
        self.notes_button.grid(row=0, column=0)
        self.notes_frame = tk.Frame(self.labelframetwo)
        self.notes_frame.configure(background='dark slate gray')
        device = config.get("section1", 'device_type')
        if (device == 'rpi'):
            self.notes_text = tk.Text(self.notes_frame,
                                  font=("TkCaptionFont", 11), foreground="PeachPuff2", width=55, height=11,
                                  background='dark slate gray',wrap= tk.WORD)
        else:
            self.notes_text = tk.Text(self.notes_frame,
                                      font=("TkCaptionFont", 14), foreground="PeachPuff2", width=75, height=13,
                                      background='dark slate gray', wrap=tk.WORD)
        self.notes_text.insert(1.0, self.video_notes)
        self.notes_text.grid(row=0)
        self.scrollbar = ttk.Scrollbar(self.notes_frame)
        self.notes_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.notes_text.yview, style='TScrollbar')

        self.scrollbar.grid(row=0,column=1,sticky="nsew")
        self.notes_frame.grid(row=1,column=0,padx=25)



if __name__== "__main__":
        app = tk.Tk()
        app.screen_width= 1000
        app.screen_height = 1000
        app.geometry("800x800")
        frame = MagicApplicationVideo(app)

        frame.grid(row=0)
        app.mainloop()










