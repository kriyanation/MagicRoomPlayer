import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import Data_Flow, configparser
from pathlib import Path


import  sys

from PIL import Image, ImageTk

import pageutils

_isLinux = sys.platform.startswith('linux')
config = configparser.RawConfigParser()
two_up = Path(__file__).resolve().parents[2]
print(str(two_up)+'/magic.cfg')
db=config.read(str(two_up)+'/magic.cfg')
imageroot = Data_Flow.imageroot
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
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        factual_content_list = Data_Flow.get_factual_content()
        factual_content_terms = factual_content_list[0]
        print(factual_content_terms)
        factual_content_descriptions = factual_content_list[1]
        print(factual_content_descriptions)
        factual_content_images = factual_content_list[2]



        self.labelframeone = ttk.Labelframe(self, text="Did you know?", relief=tk.RIDGE,style='Red.TLabelframe')
        self.labelframetwo = ttk.Labelframe(self,text="Did you know?", relief=tk.RIDGE,style='Red.TLabelframe')
        self.labelframethree = ttk.Labelframe(self, text="Did you know?", relief=tk.RIDGE,style='Red.TLabelframe')
        self.factual_term_label_one = ttk.Label(self.labelframeone, text = factual_content_terms[0], background = 'dark slate gray',foreground = 'ivory2', font=("TkCaptionFont", 18,'bold'))
        self.factual_term_label_two = ttk.Label(self.labelframetwo,text=factual_content_terms[1], background = 'dark slate gray',foreground = 'ivory2', font=("TkCaptionFont", 18,'bold'))
        self.factual_term_label_three = ttk.Label(self.labelframethree,text=factual_content_terms[2],background = 'dark slate gray', foreground = 'ivory2', font=("TkCaptionFont", 18,'bold'))

        self.factual_description_label_one = ttk.Label(self.labelframeone, text=factual_content_descriptions[0], background='dark slate gray',foreground='PeachPuff2', font=("TkFixedFont",16),wraplength = 600)
        self.factual_description_label_two = ttk.Label(self.labelframetwo,text=factual_content_descriptions[1],background='dark slate gray', foreground='PeachPuff2', font=("TkFixedFont",16),wraplength = 600)
        self.factual_description_label_three = ttk.Label(self.labelframethree,text=factual_content_descriptions[2], background='dark slate gray', foreground='PeachPuff2', font=("TkFixedFont",16),wraplength = 600)

        self.factual_image1 = factual_content_images[0]
        self.factual_image2 = factual_content_images[1]
        self.factual_image3 = factual_content_images[2]
        self.canvas_image1 = tk.Canvas(self.labelframeone,

                        bg='dark slate gray',borderwidth = 0, highlightthickness=0,relief=tk.FLAT
                                                         )
        self.canvas_image2 = tk.Canvas(self.labelframetwo,

                                    bg='dark slate gray',borderwidth = 0, highlightthickness=0,relief=tk.FLAT
                                       )
        self.canvas_image3 = tk.Canvas(self.labelframethree,

                                   bg='dark slate gray',borderwidth = 0, highlightthickness=0,relief=tk.FLAT)

        self.canvas_image1.bind("<B1-Motion>", lambda event, c=self.canvas_image1: self.paint(event,c))
        self.canvas_image1.bind('<ButtonRelease-1>', self.reset)
        self.canvas_image2.bind("<B1-Motion>", lambda event, c=self.canvas_image2: self.paint(event,c))
        self.canvas_image2.bind('<ButtonRelease-1>', self.reset)
        self.canvas_image3.bind("<B1-Motion>", lambda event, c=self.canvas_image3: self.paint(event,c))
        self.canvas_image3.bind('<ButtonRelease-1>', self.reset)
        device = config.get("section1", 'device_type')
        try:

                self.image1 = Image.open(self.factual_image1)

                self.image2 = Image.open(self.factual_image2)

                self.image3 = Image.open(self.factual_image3)

        except (FileNotFoundError , IsADirectoryError):
            messagebox.showerror("Error", "Factual Images Could not be retrieved \n e.g. "+self.factual_image1)
            print(self.factual_image1)
            print(self.factual_image2)
            print(self.factual_image3)
            parent.destroy()
            sys.exit()


        self.bind("<Configure>", self.resize_c)

        self.buttonimage = tk.PhotoImage(file="../images/speaker.png")

        self.voicebutton1 = ttk.Button(self.labelframeone, image=self.buttonimage, command=lambda: pageutils.playtextsound(factual_content_descriptions[0],'f'),style='Green.TButton')
        self.voicebutton2 = ttk.Button(self.labelframetwo,image=self.buttonimage, command=lambda: pageutils.playtextsound(factual_content_descriptions[1],'m'),style='Green.TButton')
        self.voicebutton3 = ttk.Button(self.labelframethree, image=self.buttonimage, command=lambda: pageutils.playtextsound(factual_content_descriptions[2],'f'),style='Green.TButton')


        self.factual_index = 0
        self.add_factual_panel(self.labelframeone,self.factual_term_label_one, self.factual_description_label_one,self.canvas_image1, self.voicebutton1,self.factual_image1,self.factual_index)
        self.old_x, self.old_y = None, None

    def resize_c(self,event):
        self.canvas_image1.delete("all")
        self.canvas_image2.delete("all")
        self.canvas_image3.delete("all")
        if self.factual_index == 0:
            self.image1 = self.image1.resize(
              (int(self.winfo_width()/2)-100, int(self.winfo_height()/2)-100), Image.ANTIALIAS)
            self.fimage1_display = ImageTk.PhotoImage(self.image1)
            self.canvas_image1.configure(width=int(self.winfo_width() / 2), height=int(self.winfo_height() / 2))
            self.image1_id = self.canvas_image1.create_image(0, 0, image=self.fimage1_display, anchor=tk.NW)
        elif self.factual_index == 1:
            self.image2 = self.image2.resize(
            (int(self.winfo_width() / 2)-100, int(self.winfo_height() / 2)-100), Image.ANTIALIAS)
            self.fimage2_display = ImageTk.PhotoImage(self.image2)
            self.canvas_image2.configure(width=int(self.winfo_width() / 2), height=int(self.winfo_height() / 2))
            self.image2_id = self.canvas_image2.create_image(0, 0, image=self.fimage2_display, anchor=tk.NW)
        else:
            self.image3 = self.image3.resize(
            (int(self.winfo_width() / 2)-100, int(self.winfo_height() / 2)-100), Image.ANTIALIAS)
            self.fimage3_display = ImageTk.PhotoImage(self.image3)
            self.canvas_image3.configure(width=int(self.winfo_width() / 2), height=int(self.winfo_height() / 2))
            self.image3_id = self.canvas_image3.create_image(0, 0, image=self.fimage3_display, anchor=tk.NW)



    def save_image_window(self,canvas,factualterm):
        # subprocess.run([title_image], check=False)
        canvas.postscript(file='fact_image'+factualterm+".eps")
        image = Image.open('fact_image'+factualterm+".eps")
        image.save(Data_Flow.saved_canvas+os.path.sep+"saved_images_fact_image"+factualterm+'.png','png')
        image.close()
        os.remove('fact_image'+factualterm+".eps")
        messagebox.showinfo("Information","Image saved under saved_images folder")

    def open_image_window(self, image):
        # subprocess.run([title_image], check=False)
        if sys.platform == "win32":
            os.startfile(image)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, image])

    def add_factual_panel(self,labelframe,label, description, canvas, button,image,index):
        #labelframe.grid_rowconfigure(3,weight=1)
        #labelframe.grid_columnconfigure(0, weight=1)

        labelframe.grid(row=0, column=0, padx=60, pady=0)
        self.image_frame = tk.Frame(labelframe)
        self.image_frame.configure(background='dark slate gray')
        self.new_window_image_button = ttk.Button(self.image_frame, text="Zoom Image",
                                                  command=lambda: self.open_image_window(image),
                                                  style='Green.TButton')
        self.image_save_button = ttk.Button(self.image_frame, text="Save Board",
                                            command=lambda: self.save_image_window(canvas,label.cget("text")),style='Green.TButton')
        self.labeltext=label.cget("text")
        self.desctext=description.cget("text")
        self.text_zoom_button = ttk.Button(self.image_frame, text="Zoom Text",
                                            command=lambda: self.show_text_window(self.labeltext, self.desctext),
                                            style='Green.TButton')

        self.text_zoom_button.grid(row=0, column=1, padx=10)
        self.new_window_image_button.grid(row=0,column=0,padx=10)
        self.image_save_button.grid(row=0,column=2,padx=10)


        label.grid(row=0,column=0,columnspan =2,sticky=tk.W)
        description.grid(row=1, padx=10, column=0,columnspan=3,sticky=tk.W)
        self.image_frame.grid(row=2,column=0,columnspan=3,sticky=tk.NSEW)
        self.event_generate("<Configure>")
        canvas.grid(row=3, rowspan=3,column=0, columnspan=3, padx=150, pady=5, sticky=tk.NSEW)
        button.grid(row=4, column=0, padx = 5,sticky=tk.W)
        if index == 0 or index == 1:
            self.nextfactbutton = ttk.Button(self,text="Next One !", command =lambda: self.nextfact(index),style='Green.TButton')
            self.nextfactbutton.grid(row = 1, column = 0,pady=10)

    def nextfact(self, index):
        if index == 0:
            self.factual_index = 1
            self.labelframeone.grid_forget()
            self.nextfactbutton.grid_forget()
            self.add_factual_panel(self.labelframetwo, self.factual_term_label_two, self.factual_description_label_two,
                                   self.canvas_image2,
                                   self.voicebutton2, self.factual_image2,1)
        elif index == 1:
            self.factual_index = 2
            self.labelframetwo.grid_forget()
            self.nextfactbutton.grid_forget()
            self.add_factual_panel(self.labelframethree, self.factual_term_label_three,
                                   self.factual_description_label_three, self.canvas_image3,
                                   self.voicebutton3, self.factual_image3,2)

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

    def   show_text_window(self,label,description):
      #  self.option_add('*Dialog.msg.font', 'Helvetica 30')
        top = tk.Toplevel(self)
        top.configure(background="dark slate gray")
        top.grab_set()
        top.transient(self)
        termlabel = ttk.Label(top,text=label,background='dark slate gray',foreground='ivory2',wraplength=400,font=('courier', 32, 'bold', 'italic'))
        desclabel = ttk.Label(top,text=description, background='dark slate gray', foreground='ivory2',wraplength=1000,font=('courier', 24, 'bold', 'italic'))
        closebutton = ttk.Button(top,text="Close",command=top.destroy,style="Green.TButton")

        voicebutton_top= ttk.Button(top, image=self.buttonimage,
                                   command=lambda: pageutils.playtextsound(description),
                                   style='Green.TButton')

        termlabel.pack()
        desclabel.pack()
        voicebutton_top.pack(side=tk.RIGHT)
        closebutton.pack()
       # self.option_clear()



if __name__== "__main__":
        app = tk.Tk()
        app.geometry("600x600")
        app.screen_width = 600
        app.screen_height = 600
        frame = MagicFactualPage(app)

        frame.grid(row=0)
        app.mainloop()










