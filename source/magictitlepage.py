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
        s = ttk.Style(self)
        s.configure('Green.TButton', background='dark slate gray', foreground='PeachPuff2')
        s.map('Green.TButton', background=[('active', '!disabled', 'dark olive green'), ('pressed', 'PeachPuff2')],
              foreground=[('pressed', 'PeachPuff2'), ('active', 'PeachPuff2')])

        s.configure('TScrollbar', background='dark slate gray', foreground='dark slate gray')
        s.map('TScrollbar', background=[('active', '!disabled', 'dark olive green'), ('disabled', 'dark slate gray')],
              foreground=[('active', 'PeachPuff2'), ('disabled', 'dark slate gray')])
        print(type(parent).__name__)
        self.parent_window = parent
        self.old_x, self.old_y = None, None
        self.configure(background='dark slate gray')
        self.quote_text = Data_Flow.get_Quote()
        self.quote_textwidget = tk.Text(self, borderwidth=0,highlightthickness=0,relief=tk.FLAT,wrap=tk.WORD,font= ('TkDefaultFont',12,'bold'), bd=2,foreground = 'PeachPuff2', width=90,height=2,background=
                                     'dark slate gray')

        self.counter = 0
        pageutils.animate_text( self, self.quote_text, self.counter,self.quote_textwidget,len(self.quote_text)-1)

        self.quote_textwidget.pack(padx=30,anchor = tk.NW)

        args = []
        if _isLinux:
            args.append('--no-xlib')
        self.Instance = vlc.Instance(args)
        self.player = self.Instance.media_player_new()

        parent.bind("<Configure>", self.OnConfigure)  # catch window resize, etc.
        parent.update()

    def paint(self, event):

        #x1, y1 = (event.x - 1), (event.y - 1)
        #x2, y2 = (event.x + 1), (event.y + 1)
        #self.canvas.create_oval(x1, y1, x2, y2, fill='white')

        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                               width=5, fill='bisque2',
                                               capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def title_intro(self):
        self.playtextsound(self.quote_text)
        time.sleep(2)
        title_text = Data_Flow.get_Title()
        self.topic_label = ttk.Label(self, text = title_text,font= ('TkDefaultFont', 16), foreground = 'PeachPuff2',background = 'dark slate gray', wraplength=self.parent_window.screen_width/2.5)
        self.topic_label.pack(pady=30,anchor = tk.CENTER)
        title_image = Data_Flow.get_title_image()
        self.canvas = tk.Canvas(self,
                        width=self.parent_window.screen_width/1.5,
                        height=self.parent_window.screen_height/2.0,background='dark slate gray',borderwidth = 0, highlightthickness=0,relief=tk.FLAT)
        self.canvas.pack( padx=10, anchor = tk.CENTER)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.img = Image.open(title_image)
        self.img = self.img.resize((400,400))
        self.img1 = ImageTk.PhotoImage(self.img)
        self.title_image_id = self.canvas.create_image(self.winfo_width()/2+150, self.parent_window.screen_height/3.5, image=self.img1)
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
        self.appHighlightFont = font.Font(family='Comic Sans', size=14, weight='bold')
       # b = '\u0B9A\u0BC1\u0BB5\u0BBE\u0B9A'
        b = '\u0936\u094D\u0935\u0938\u0928\20\u092A\u094D\u0930\u0923\u093E\u0932\u0940'

        self.video_note_text = tk.Text(self,pady=30, borderwidth=0,highlightthickness=0,relief=tk.SUNKEN,wrap= tk.WORD,font=self.appHighlightFont, foreground = "PeachPuff2",background ='dark slate gray', width=80, height=40)
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

    def playtextsound(self,text):
        engine = pyttsx3.init(driverName='espeak')
        engine.setProperty('voice', 'english+m2')
        engine.setProperty('rate', 150)
        engine.say(text)
        engine.runAndWait()






