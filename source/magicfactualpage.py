import tkinter as tk
from tkinter import ttk
import Data_Flow, configparser


import  sys

from PIL import Image, ImageTk

import pageutils

_isLinux = sys.platform.startswith('linux')
config = configparser.RawConfigParser()
config.read('magic.cfg')
class MagicFactualPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.config({'bg':'blue'})
        self.configure(background='dark slate gray')
        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background='dark slate gray')
        s.configure('Red.TLabelframe.Label', font=('courier', 12, 'bold', 'italic'))
        s.configure('Red.TLabelframe.Label', foreground='PeachPuff2')
        s.configure('Red.TLabelframe.Label', background='dark slate gray')

        s.configure('Green.TButton', background='dark slate gray', foreground='PeachPuff2')
        s.map('Green.TButton', background=[('active', '!disabled', 'dark olive green'), ('pressed', 'PeachPuff2')],
              foreground=[('pressed', 'PeachPuff2'), ('active', 'PeachPuff2')])

        factual_content_list = Data_Flow.get_factual_content()
        factual_content_terms = factual_content_list[0]
        print(factual_content_terms)
        factual_content_descriptions = factual_content_list[1]
        print(factual_content_descriptions)
        factual_content_images = factual_content_list[2]


        self.labelframeone = ttk.Labelframe(self, width = parent.screen_width/1.8, height = parent.screen_height/1.5, text="Did you know?", relief=tk.RIDGE,style='Red.TLabelframe')
        self.labelframetwo = ttk.Labelframe(self, width = parent.screen_width/1.8, height = parent.screen_height/1.5,text="Did you know?", relief=tk.RIDGE,style='Red.TLabelframe')
        self.labelframethree = ttk.Labelframe(self,width = parent.screen_width/1.8, height = parent.screen_height/1.5, text="Did you know?", relief=tk.RIDGE,style='Red.TLabelframe')
        self.factual_term_label_one = ttk.Label(self.labelframeone, text = factual_content_terms[0], background = 'dark slate gray',foreground = 'ivory2', font=("TkCaptionFont", 15,'bold'))
        self.factual_term_label_two = ttk.Label(self.labelframetwo,text=factual_content_terms[1], background = 'dark slate gray',foreground = 'ivory2', font=("TkCaptionFont", 15,'bold'))
        self.factual_term_label_three = ttk.Label(self.labelframethree,text=factual_content_terms[2],background = 'dark slate gray', foreground = 'ivory2', font=("TkCaptionFont", 15,'bold'))

        self.factual_description_label_one = ttk.Label(self.labelframeone, text=factual_content_descriptions[0], background='dark slate gray',foreground='PeachPuff2', font=("TkFixedFont",12),wraplength = 400)
        self.factual_description_label_two = ttk.Label(self.labelframetwo,text=factual_content_descriptions[1],background='dark slate gray', foreground='PeachPuff2', font=("TkFixedFont",12),wraplength = 400)
        self.factual_description_label_three = ttk.Label(self.labelframethree,text=factual_content_descriptions[2], background='dark slate gray', foreground='PeachPuff2', font=("TkFixedFont",12),wraplength = 400)






        factual_image1 = factual_content_images[0]
        factual_image2 = factual_content_images[1]
        factual_image3 = factual_content_images[2]
        self.canvas_image1 = tk.Canvas(self.labelframeone,
                        width=parent.screen_width/2.9,
                        height=parent.screen_height/2.5,bg='dark slate gray',borderwidth = 0, highlightthickness=0,relief=tk.FLAT
                                                         )
        self.canvas_image2 = tk.Canvas(self.labelframetwo,
                                   width=parent.screen_width / 2.9,
                                   height=parent.screen_height / 2.6, bg='dark slate gray',borderwidth = 0, highlightthickness=0,relief=tk.FLAT
                                       )
        self.canvas_image3 = tk.Canvas(self.labelframethree,
                                   width=parent.screen_width / 2.9,
                                   height=parent.screen_height / 2.5,bg='dark slate gray',borderwidth = 0, highlightthickness=0,relief=tk.FLAT)

        self.canvas_image1.bind("<B1-Motion>", lambda event, c=self.canvas_image1: self.paint(event,c))
        self.canvas_image1.bind('<ButtonRelease-1>', self.reset)
        self.canvas_image2.bind("<B1-Motion>", lambda event, c=self.canvas_image2: self.paint(event,c))
        self.canvas_image2.bind('<ButtonRelease-1>', self.reset)
        self.canvas_image3.bind("<B1-Motion>", lambda event, c=self.canvas_image3: self.paint(event,c))
        self.canvas_image3.bind('<ButtonRelease-1>', self.reset)
        device = config.get("section1", 'device_type')
        if (device == 'rpi'):
            image1 = Image.open(factual_image1)
            image1.thumbnail((300,300))
            image2 = Image.open(factual_image2)
            image2.thumbnail((300, 300))
            image3 = Image.open(factual_image3)
            image3.thumbnail((300, 300))
        else:
            image1 = Image.open(factual_image1)
            image1.thumbnail((400, 400))
            image2 = Image.open(factual_image2)
            image2.thumbnail((400, 400))
            image3 = Image.open(factual_image3)
            image3.thumbnail((400, 400))
        self.fimage1 = image1 # Image.open("../images/image1_thumbnail")
        self.fimage2 = image2
        self.fimage3 = image3
        self.fimage1_display = ImageTk.PhotoImage(self.fimage1)
        self.fimage2_display = ImageTk.PhotoImage(self.fimage2)
        self.fimage3_display = ImageTk.PhotoImage(self.fimage3)
        self.image1_id = self.canvas_image1.create_image(parent.screen_width/6.7, parent.screen_height/7, image=self.fimage1_display)
        self.image2_id = self.canvas_image2.create_image(parent.screen_width/6.7, parent.screen_height/7, image=self.fimage2_display)
        self.image3_id = self.canvas_image3.create_image(parent.screen_width/6.7, parent.screen_height/7, image=self.fimage3_display)

        self.buttonimage = tk.PhotoImage(file="../images/speaker.png")

        self.voicebutton1 = ttk.Button(self.labelframeone, image=self.buttonimage, command=lambda: pageutils.playtextsound(factual_content_descriptions[0],'f'),style='Green.TButton')
        self.voicebutton2 = ttk.Button(self.labelframetwo,image=self.buttonimage, command=lambda: pageutils.playtextsound(factual_content_descriptions[1],'m'),style='Green.TButton')
        self.voicebutton3 = ttk.Button(self.labelframethree, image=self.buttonimage, command=lambda: pageutils.playtextsound(factual_content_descriptions[2],'f','kannada'),style='Green.TButton')

        self.add_factual_panel(self.labelframeone,self.factual_term_label_one, self.factual_description_label_one,self.canvas_image1, self.voicebutton1,0)
        self.old_x, self.old_y = None, None



    def add_factual_panel(self,labelframe,label, description, canvas, button,index):
        labelframe.grid_propagate(False)
        labelframe.grid(row=0, column=0, padx=60, pady=0)
        label.grid(row=0,column=1,sticky=tk.NSEW)
        description.grid(row=1, padx=10, column=1,sticky=tk.NSEW)
        canvas.grid(row=2, column=0, columnspan=3, padx=150, pady=15, sticky=tk.NSEW)
        button.grid(row=3, column=0, padx = 5,sticky=tk.SW)
        if index == 0 or index == 1:
            self.nextfactbutton = ttk.Button(self,text="Next One !", command =lambda: self.nextfact(index),style='Green.TButton')
            self.nextfactbutton.grid(row = 1, column = 0,pady=10)

    def nextfact(self, index):
        if index == 0:
            self.labelframeone.grid_forget()
            self.nextfactbutton.grid_forget()
            self.add_factual_panel(self.labelframetwo, self.factual_term_label_two, self.factual_description_label_two,
                                   self.canvas_image2,
                                   self.voicebutton2, 1)
        elif index == 1:
            self.labelframetwo.grid_forget()
            self.nextfactbutton.grid_forget()
            self.add_factual_panel(self.labelframethree, self.factual_term_label_three,
                                   self.factual_description_label_three, self.canvas_image3,
                                   self.voicebutton3, 2)
        else:
            self.nextfactbutton.grid_forget()



    def reset(self, event):
        self.old_x, self.old_y = None, None

    def paint(self, event, canvas):

        # x1, y1 = (event.x - 1), (event.y - 1)
        # x2, y2 = (event.x + 1), (event.y + 1)
        # self.canvas.create_oval(x1, y1, x2, y2, fill='white')

        if self.old_x and self.old_y:
            canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=5, fill='bisque2',
                                    capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y


if __name__== "__main__":
        app = tk.Tk()
        app.geometry("600x600")
        app.screen_width = 600
        app.screen_height = 600
        frame = MagicFactualPage(app)

        frame.grid(row=0)
        app.mainloop()










