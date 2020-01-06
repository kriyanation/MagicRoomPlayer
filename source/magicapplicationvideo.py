import tkinter as tk
from tkinter import ttk, font, filedialog
import Data_Flow
import pyttsx3
import vlc, sys, time, subprocess
import unicodedata
import scroll_bars
from tkinter.colorchooser import askcolor

import PIL
from PIL import Image, ImageTk

import pageutils

_isLinux = sys.platform.startswith('linux')

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'

class MagicApplicationVideo(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.application_video_info = Data_Flow.get_application_video()
        self.video_link = "../videos/"+self.application_video_info[0]
        self.video_notes = self.application_video_info[1]



        self.labelframeone = ttk.Labelframe(self, width = parent.screen_width/1.5, height = parent.screen_height/2.5, text="Insightful Video", relief=tk.RAISED)
        self.labelframetwo = ttk.Labelframe(self, width = parent.screen_width/1.5, height = parent.screen_height/2.5,text="Things to Note", relief=tk.RIDGE)
        self.play_button = ttk.Button(self.labelframeone, text="Play", command= self.play_video)
        self.pause_button = ttk.Button(self.labelframeone, text="Pause", command= self.pause_video)
        self.new_screen_button = ttk.Button(self.labelframeone, text="New Window", command=self.new_window)
        self.video_frame = tk.Frame(self.labelframeone, width = parent.screen_width/1.8, height= parent.screen_height/3)

        self.play_button.grid(row=0,column=0)
        self.pause_button.grid(row=0,column=1)
        self.new_screen_button.grid(row=0, column=2)
        self.video_frame.grid(row=1,columnspan = 3)
        self.labelframeone.grid_propagate(False)
        self.labelframetwo.grid_propagate(False)
        self.labelframeone.grid(row=0, pady=20, padx = 20)
        self.labelframetwo.grid(row=1, pady= 20, padx = 20)

        args = []
        if _isLinux:
            args.append('--no-xlib')
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()

        parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
        parent.update()

        self.fill_video_frame()
        self.fill_notes_frame(parent.screen_width)


    def play_video(self):
         self.player.play()




    def new_window(self):
        self.player.stop()
        subprocess.Popen(['vlc', '-vvv', self.video_link])

    def pause_video(self):
        self.player.pause()
       #self.player.set_fullscreen(False)

    def OnConfigure(self, *unused):
        """Some widget configuration changed.
        """
        # <https://www.Tcl.Tk/man/tcl8.6/TkCmd/bind.htm#M12>
        self._geometry = ''  # force .OnResize in .OnTick, recursive?


    def fill_video_frame(self):
        self.media = self.Instance.media_new(str(self.video_link))  # Path, unicode
        self.player.set_media(self.media)
        player_frame_info = self.video_frame.winfo_id()  # .winfo_visualid()?
        self.player.set_xwindow(player_frame_info)
       # self.player.play()

    def fill_notes_frame(self,width):
        self.notes_label = ttk.Label(self.labelframetwo, text=self.video_notes,
                                         font=("TkCaptionFont", 14),foreground="blue", wraplength=width/1.8)
        self.notes_button = ttk.Button(self.labelframetwo, text="Voice Notes", command = lambda:pageutils.playtextsound(self.video_notes))
        self.notes_button.grid(row=0, column=1)
        self.notes_label.grid(row=1)







if __name__== "__main__":
        app = tk.Tk()
        app.geometry("800x800")
        frame = MagicApplicationVideo(app)

        frame.grid(row=0)
        app.mainloop()










