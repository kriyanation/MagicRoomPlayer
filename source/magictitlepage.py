import tkinter as tk
from tkinter import ttk
import Data_Flow
import pyttsx3
import vlc, sys

import PIL
from PIL import Image, ImageTk
_isLinux = sys.platform.startswith('linux')

class MagicTitlePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.quote_text = Data_Flow.get_Quote()
        self.quote_label = ttk.Label(self, font= ('TkDefaultFont', 14), foreground = 'blue', wraplength=800)
        self.counter = 0
        #self.animateQuote( self.quote_text, self.counter)
        self.quote_label.pack(anchor = tk.NW)
        args = []
        if _isLinux:
            args.append('--no-xlib')
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()

        parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
        parent.update()

    def title_intro(self):

        title_text = Data_Flow.get_Title()
        self.topic_label = ttk.Label(self, text = title_text,font= ('TkDefaultFont', 14), foreground = 'brown', wraplength=500)
        self.topic_label.pack(anchor = tk.CENTER)
        title_image = Data_Flow.get_title_image()
        self.canvas = tk.Canvas(self,
                        width=600,
                        height=600)
        self.canvas.pack( anchor = tk.CENTER, fill=tk.BOTH, expand = tk.YES)
        self.img = Image.open(title_image)
        self.img = self.img.resize((500,500))
        self.img1 = ImageTk.PhotoImage(self.img)
        self.title_image_id = self.canvas.create_image(self.winfo_width()/2, 300, image=self.img1)
        self.playtextsound(title_text)

    def title_video(self):
        self.title_video = Data_Flow.get_title_video()
        self.media = self.Instance.media_new(str(self.title_video))  # Path, unicode
        self.player.set_media(self.media)
        self.canvas.delete(self.title_image_id)
        player_frame_info = self.canvas.winfo_id()  # .winfo_visualid()?
        self.player.set_xwindow(player_frame_info)
        self.player.play()

    def OnConfigure(self, *unused):
        """Some widget configuration changed.
        """
        # <https://www.Tcl.Tk/man/tcl8.6/TkCmd/bind.htm#M12>
        self._geometry = ''  # force .OnResize in .OnTick, recursive?






    def animateQuote(self, quote_text, counter):
        print(quote_text)
        self.quote_label.config(text=quote_text[:counter])
        if counter > 150:
            self.playtextsound(quote_text)
            return
        self.after(50, lambda: self.animateQuote(quote_text,counter + 1))

    def playtextsound(self,text):
        engine = pyttsx3.init(driverName='espeak')
        engine.setProperty('voice', 'english+m2')
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()



