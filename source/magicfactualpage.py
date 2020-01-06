import tkinter as tk
from tkinter import ttk, font
import Data_Flow
import pyttsx3
import vlc, sys, time
import unicodedata
import scroll_bars

import PIL
from PIL import Image, ImageTk

import pageutils

_isLinux = sys.platform.startswith('linux')

class MagicFactualPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.config({'bg':'blue'})

        factual_content_list = Data_Flow.get_factual_content()
        factual_content_terms = factual_content_list[0]
        print(factual_content_terms)
        factual_content_descriptions = factual_content_list[1]
        print(factual_content_descriptions)
        factual_content_images = factual_content_list[2]


        self.labelframeone = ttk.Labelframe(self, width = parent.screen_width/1.5, height = parent.screen_height/2, text="Did you know?", relief=tk.RIDGE)
        self.labelframetwo = ttk.Labelframe(self, width = parent.screen_width/1.5, height = parent.screen_height/2,text="Did you know?", relief=tk.RIDGE)
        self.labelframethree = ttk.Labelframe(self,width = parent.screen_width/1.5, height = parent.screen_height/2, text="Did you know?", relief=tk.RIDGE)
        self.factual_term_label_one = ttk.Label(self.labelframeone, text = factual_content_terms[0], foreground = 'brown', font=("TkCaptionFont", 14))
        self.factual_term_label_two = ttk.Label(self.labelframetwo,text=factual_content_terms[1], foreground = 'brown', font=("TkCaptionFont", 14))
        self.factual_term_label_three = ttk.Label(self.labelframethree,text=factual_content_terms[2], foreground = 'brown', font=("TkCaptionFont", 14))

        self.factual_description_label_one = ttk.Label(self.labelframeone, text=factual_content_descriptions[0], foreground='blue', font=("TkFixedFont",12),wraplength = parent.screen_width/2.5)
        self.factual_description_label_two = ttk.Label(self.labelframetwo,text=factual_content_descriptions[1], foreground='blue', font=("TkFixedFont",12),wraplength = parent.screen_width/2.5)
        self.factual_description_label_three = ttk.Label(self.labelframethree,text=factual_content_descriptions[2], foreground='blue', font=("TkFixedFont",12),wraplength = parent.screen_width/2.5)






        factual_image1 = "../images/"+factual_content_images[0]
        factual_image2 = "../images/" + factual_content_images[1]
        factual_image3 = "../images/" + factual_content_images[2]
        self.canvas_image1 = tk.Canvas(self.labelframeone,
                        width=parent.screen_width/3.5,
                        height=parent.screen_height/3)
        self.canvas_image2 = tk.Canvas(self.labelframetwo,
                                   width=parent.screen_width / 3.5,
                                   height=parent.screen_height / 3)
        self.canvas_image3 = tk.Canvas(self.labelframethree,
                                   width=parent.screen_width / 3.5,
                                   height=parent.screen_height / 3)

        self.canvas_image1.bind("<B1-Motion>", self.paint)
        self.canvas_image2.bind("<B1-Motion>", self.paint)
        self.canvas_image3.bind("<B1-Motion>", self.paint)
        image1 = Image.open(factual_image1)
        image1.thumbnail((300,300))
        image2 = Image.open(factual_image2)
        image2.thumbnail((300, 300))
        image3 = Image.open(factual_image3)
        image3.thumbnail((300, 300))
        self.fimage1 = image1 # Image.open("../images/image1_thumbnail")
        self.fimage2 = image2
        self.fimage3 = image3
        self.fimage1_display = ImageTk.PhotoImage(self.fimage1)
        self.fimage2_display = ImageTk.PhotoImage(self.fimage2)
        self.fimage3_display = ImageTk.PhotoImage(self.fimage3)
        self.image1_id = self.canvas_image1.create_image(parent.screen_width/6, parent.screen_height/10, image=self.fimage1_display)
        self.image2_id = self.canvas_image2.create_image(parent.screen_width/6, parent.screen_height/10, image=self.fimage2_display)
        self.image3_id = self.canvas_image3.create_image(parent.screen_width/6, parent.screen_height/10, image=self.fimage3_display)

        self.voicebutton1 = ttk.Button(self.labelframeone, text="Read Aloud", command=lambda: pageutils.playtextsound(factual_content_descriptions[0],'f'))
        self.voicebutton2 = ttk.Button(self.labelframetwo,text="Read Aloud", command=lambda: pageutils.playtextsound(factual_content_descriptions[1],'m'))
        self.voicebutton3 = ttk.Button(self.labelframethree, text="Read Aloud", command=lambda: pageutils.playtextsound(factual_content_descriptions[2],'f'))

        self.add_factual_panel(self.labelframeone,self.factual_term_label_one, self.factual_description_label_one,self.canvas_image1, self.voicebutton1,0)




    def add_factual_panel(self,labelframe,label, description, canvas, button,index):
        labelframe.grid_propagate(False)
        labelframe.grid(row=index, column=0, padx=60, pady=200)
        label.grid(row=0,column=0, padx=30)
        description.grid(row=0, column=1)
        canvas.grid(row=1,column=0, columnspan=2)
        button.grid(row=0, column=2, sticky=tk.E)
        if index == 0 or index == 1:
            self.nextfactbutton = ttk.Button(self,text="Next One !", command =lambda: self.nextfact(index))
            self.nextfactbutton.grid(row = 1, column = 2, sticky = tk.SE)

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

    def paint(self, event):

        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        event.widget.create_oval(x1, y1, x2, y2, fill='black')


if __name__== "__main__":
        app = tk.Tk()
        app.geometry("600x600")
        frame = MagicFactualPage(app)

        frame.grid(row=0)
        app.mainloop()










