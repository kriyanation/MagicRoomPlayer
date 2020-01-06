import tkinter as tk
from tkinter import ttk, font
import Data_Flow
import pyttsx3
import vlc, sys, time
import pageutils

import PIL
from PIL import Image, ImageTk
_isLinux = sys.platform.startswith('linux')

class MagicTitlePage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        print(type(parent).__name__)
        self.parent_window = parent
        self.quote_text = Data_Flow.get_Quote()
        self.quote_label = ttk.Label(self, font= ('TkDefaultFont', 14), foreground = 'blue', wraplength=parent.screen_width/1.5)
        self.counter = 0
        pageutils.animate_text( self, self.quote_text, self.counter,self.quote_label,150)
        self.quote_label.pack(anchor = tk.NW)

        args = []
        if _isLinux:
            args.append('--no-xlib')
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()

        parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
        parent.update()

    def paint(self, event):

        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        self.canvas.create_oval(x1, y1, x2, y2, fill='black')

    def title_intro(self):
        self.playtextsound(self.quote_text)
        time.sleep(2)
        title_text = Data_Flow.get_Title()
        self.topic_label = ttk.Label(self, text = title_text,font= ('TkDefaultFont', 16), foreground = 'brown', wraplength=self.parent_window.screen_width/2.5)
        self.topic_label.pack(pady=30,anchor = tk.CENTER)
        title_image = "../images/"+Data_Flow.get_title_image()
        self.canvas = tk.Canvas(self,
                        width=self.parent_window.screen_width/1.5,
                        height=self.parent_window.screen_height/1.5)
        self.canvas.pack( padx=10, anchor = tk.CENTER)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.img = Image.open(title_image)
        self.img = self.img.resize((500,500))
        self.img1 = ImageTk.PhotoImage(self.img)
        self.title_image_id = self.canvas.create_image(self.winfo_width()/2+150, self.parent_window.screen_height/4, image=self.img1)
        pageutils.playtextsound(title_text)

    def title_video(self):
        self.title_video = Data_Flow.get_title_video()
        self.media = self.Instance.media_new(str(self.title_video))  # Path, unicode
        self.player.set_media(self.media)
        self.canvas.delete(self.title_image_id)
        player_frame_info = self.canvas.winfo_id()  # .winfo_visualid()?
        self.player.set_xwindow(player_frame_info)
        self.player.play()
        video_notes_info = Data_Flow.get_Running_Notes()
        video_notes = video_notes_info[0]
        self.appHighlightFont = font.Font(family='Comic Sans', size=16, weight='bold')
       # b = '\u0B9A\u0BC1\u0BB5\u0BBE\u0B9A'
        b = '\u0936\u094D\u0935\u0938\u0928\20\u092A\u094D\u0930\u0923\u093E\u0932\u0940'

        self.video_note_label = ttk.Label(self, text = video_notes ,font=self.appHighlightFont, foreground = "blue4", wraplength = 900)
        self.video_note_label.pack(anchor = tk.S, fill = tk.Y)
        pageutils.animate_text(self, video_notes,0,self.video_note_label,self.parent_window.screen_width/3)


    def OnConfigure(self, *unused):
        """Some widget configuration changed.
        """
        # <https://www.Tcl.Tk/man/tcl8.6/TkCmd/bind.htm#M12>
        self._geometry = ''  # force .OnResize in .OnTick, recursive?






    def animate_text(self, text, counter,label, counter_max):
        print(text)
        label.config(text=text[:counter])
        if counter > counter_max:
            #self.playtextsound(quote_text)
            return
        self.after(100, lambda: self.animate_text(text,counter + 1,label,counter_max))

    def playtextsound(self,text):
        engine = pyttsx3.init(driverName='espeak')
        engine.setProperty('voice', 'english+m2')
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()



