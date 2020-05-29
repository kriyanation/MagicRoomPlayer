import os
import subprocess
import threading

import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from PIL import Image, ImageTk

import Data_Flow_Player
import pageutils
import tooltip
import logging

logger = logging.getLogger("MagicLogger")
_isLinux = sys.platform.startswith('linux')

class MagicFactualPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.config({'bg':'blue'})
        logger.info("Inside Factual Page Initialize")
        self.parent = parent
        self.configure(background='deepskyblue4')
        s = ttk.Style(self)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        factual_content_list = Data_Flow_Player.get_factual_content()
        factual_content_terms = factual_content_list[0]
        print(factual_content_terms)
        factual_content_descriptions = factual_content_list[1]
        print(factual_content_descriptions)
        factual_content_images = factual_content_list[2]
        self.pen_color = 'bisque2'
        self.buttonnextimage = tk.PhotoImage(file="../images/arrows_next.png")
        self.buttonbackimage = tk.PhotoImage(file="../images/arrows_back.png")


        self.labelframeone = ttk.Labelframe(self, text="Did you know?", relief=tk.RIDGE,style='Red.TLabelframe')
        self.labelframetwo = ttk.Labelframe(self,text="Did you know?", relief=tk.RIDGE,style='Red.TLabelframe')
        self.labelframethree = ttk.Labelframe(self, text="Did you know?", relief=tk.RIDGE,style='Red.TLabelframe')
        self.factual_term_label_one = ttk.Label(self.labelframeone, text = factual_content_terms[0], background = 'deepskyblue4',foreground = 'ivory2', font=("helvetica", 18,'bold'))
        self.factual_term_label_two = ttk.Label(self.labelframetwo,text=factual_content_terms[1], background = 'deepskyblue4',foreground = 'ivory2', font=("helvetica", 18,'bold'))
        self.factual_term_label_three = ttk.Label(self.labelframethree,text=factual_content_terms[2],background = 'deepskyblue4', foreground = 'ivory2', font=("helvetica", 18,'bold'))


        self.factual_description_label_one = ttk.Label(self.labelframeone, text=factual_content_descriptions[0].strip(), background='deepskyblue4',foreground='white', font=("helvetica",16,'bold'),wraplength = 600)
        self.factual_description_label_two = ttk.Label(self.labelframetwo,text=factual_content_descriptions[1],background='deepskyblue4', foreground='white', font=("helvetica",16,'bold'),wraplength = 600)
        self.factual_description_label_three = ttk.Label(self.labelframethree,text=factual_content_descriptions[2], background='deepskyblue4', foreground='white', font=("helvetica",16,'bold'),wraplength = 600)

        self.factual_image1 = factual_content_images[0]
        self.factual_image2 = factual_content_images[1]
        self.factual_image3 = factual_content_images[2]
        self.canvas_image1 = tk.Canvas(self.labelframeone,

                        bg='deepskyblue4',borderwidth = 0, highlightthickness=0,relief=tk.FLAT
                                                         )
        self.popup_menu_1 = tk.Menu(self.canvas_image1, background='deepskyblue4', foreground='white')
        self.popup_menu_1.add_command(label="Dark", command=self.switch_to_dark)
        self.popup_menu_1.add_command(label="Light", command=self.switch_to_light)
        self.popup_menu_1.add_command(label="Text")
        self.canvas_image1.bind('<Button-3>', self.show_popup_menu1)
        self.canvas_image2 = tk.Canvas(self.labelframetwo,

                                    bg='deepskyblue4',borderwidth = 0, highlightthickness=0,relief=tk.FLAT
                                       )
        self.popup_menu_2 = tk.Menu(self.canvas_image2, background='deepskyblue4', foreground='white')
        self.popup_menu_2.add_command(label="Dark", command=self.switch_to_dark)
        self.popup_menu_2.add_command(label="Light", command=self.switch_to_light)
        self.popup_menu_2.add_command(label="Text")
        self.canvas_image2.bind('<Button-3>', self.show_popup_menu2)
        self.canvas_image3 = tk.Canvas(self.labelframethree,

                                   bg='deepskyblue4',borderwidth = 0, highlightthickness=0,relief=tk.FLAT)
        self.popup_menu_3 = tk.Menu(self.canvas_image3, background='deepskyblue4', foreground='white')
        self.popup_menu_3.add_command(label="Dark", command=self.switch_to_dark)
        self.popup_menu_3.add_command(label="Light", command=self.switch_to_light)
        self.popup_menu_3.add_command(label="Text")
        self.canvas_image3.bind('<Button-3>', self.show_popup_menu3)

        self.canvas_image1.bind("<B1-Motion>", lambda event, c=self.canvas_image1: self.paint(event,c))
        self.canvas_image1.bind('<ButtonRelease-1>', self.reset)
        self.canvas_image2.bind("<B1-Motion>", lambda event, c=self.canvas_image2: self.paint(event,c))
        self.canvas_image2.bind('<ButtonRelease-1>', self.reset)
        self.canvas_image3.bind("<B1-Motion>", lambda event, c=self.canvas_image3: self.paint(event,c))
        self.canvas_image3.bind('<ButtonRelease-1>', self.reset)
        device = "laptop"
        try:

                self.image1 = Image.open(self.factual_image1)

                self.image2 = Image.open(self.factual_image2)

                self.image3 = Image.open(self.factual_image3)

        except (FileNotFoundError , IsADirectoryError):
            messagebox.showerror("Error", "Factual Images Could not be retrieved \n e.g. "+self.factual_image1)
            print(self.factual_image1)
            print(self.factual_image2)
            print(self.factual_image3)
            logger.exception("Factual Images cannot be retrieved")


        self.bind("<Configure>", self.resize_c)

        self.buttonimage = tk.PhotoImage(file="../images/speaker.png")

        self.voicebutton1 = ttk.Button(self.labelframeone, image=self.buttonimage, command=lambda: self.playtextsound(factual_content_descriptions[0],'f'),style='Green.TButton')
        self.voicebutton2 = ttk.Button(self.labelframetwo,image=self.buttonimage, command=lambda: self.playtextsound(factual_content_descriptions[1],'m'),style='Green.TButton')
        self.voicebutton3 = ttk.Button(self.labelframethree, image=self.buttonimage, command=lambda: self.playtextsound(factual_content_descriptions[2],'f'),style='Green.TButton')

        self.voicebutton1.tooltip = tooltip.ToolTip(self.voicebutton1, "Read Aloud")
        self.voicebutton2.tooltip = tooltip.ToolTip(self.voicebutton2, "Read Aloud")
        self.voicebutton3.tooltip = tooltip.ToolTip(self.voicebutton3, "Read Aloud")
        self.factual_index = 0
        self.add_factual_panel(self.labelframeone,self.factual_term_label_one, self.factual_description_label_one,self.canvas_image1, self.voicebutton1,self.factual_image1,self.factual_index)
        self.old_x, self.old_y = None, None


    def paint_text(self,event,canvas):
        logger.info("Factual Page - Paint Text")
        answer = simpledialog.askstring("Text to add", "Add text to the location",
                                        parent=self.parent)
        canvas.create_text(event.x,event.y,font=("comic sans", 15, "bold"),text=answer,fill=self.pen_color)

    def show_popup_menu1(self, event):

        logger.info("Factual Page - Pop-up menu 1")
        self.popup_menu_1.tk_popup(event.x_root, event.y_root)
        self.popup_menu_1.entryconfig("Text",command=lambda:self.paint_text(event,self.canvas_image1))
    def show_popup_menu2(self, event):
        logger.info("Factual Page - Pop-up menu 2")
        self.popup_menu_2.tk_popup(event.x_root, event.y_root)
        self.popup_menu_2.entryconfig("Text",command=lambda:self.paint_text(event,self.canvas_image2))
    def show_popup_menu3(self, event):
        logger.info("Factual Page - Pop-up menu 3")
        self.popup_menu_3.tk_popup(event.x_root, event.y_root)
        self.popup_menu_3.entryconfig("Text",command=lambda:self.paint_text(event,self.canvas_image3))

    def resize_c(self,event):
        logger.info("Factual Page - Resize")
        self.canvas_image1.delete("all")
        self.canvas_image2.delete("all")
        self.canvas_image3.delete("all")
        if self.factual_index == 0 and self.winfo_width()/2.1 - 100> 0 and self.winfo_height()/1.6 -100 > 0:
            self.image1 = self.image1.resize(
                (int(self.winfo_width()/2.1)-100, int(self.winfo_height()/1.6)-100), Image.ANTIALIAS)
            self.fimage1_display = ImageTk.PhotoImage(self.image1)
            self.canvas_image1.configure(width=int(self.winfo_width() / 2.1), height=int(self.winfo_height() / 1.6))
            self.image1_id = self.canvas_image1.create_image(0, 0, image=self.fimage1_display, anchor=tk.NW)
        elif self.factual_index == 1 and self.winfo_width()/2.1 - 100> 0 and self.winfo_height()/1.6 -100 > 0:
            self.image2 = self.image2.resize(
            (int(self.winfo_width() / 2.1)-100, int(self.winfo_height() / 1.6)-100), Image.ANTIALIAS)
            self.fimage2_display = ImageTk.PhotoImage(self.image2)
            self.canvas_image2.configure(width=int(self.winfo_width() / 2.1), height=int(self.winfo_height() / 1.6))
            self.image2_id = self.canvas_image2.create_image(0, 0, image=self.fimage2_display, anchor=tk.NW)
        elif self.winfo_width()/2.1 - 100> 0 and self.winfo_height()/1.6 -100:
            self.image3 = self.image3.resize(
            (int(self.winfo_width() / 2.1)-100, int(self.winfo_height() / 1.6)-100), Image.ANTIALIAS)
            self.fimage3_display = ImageTk.PhotoImage(self.image3)
            self.canvas_image3.configure(width=int(self.winfo_width() / 2.1), height=int(self.winfo_height() / 1.6))
            self.image3_id = self.canvas_image3.create_image(0, 0, image=self.fimage3_display, anchor=tk.NW)


    def switch_to_dark(self):
        self.pen_color = 'gray26'

    def switch_to_light(self):
        self.pen_color = 'bisque2'


    def save_image_window(self,canvas,factualterm):
        # subprocess.run([title_image], check=False)
        logger.info("Factual Page - save_image_window")
        canvas.postscript(file='fact_image'+factualterm+".eps")
        image = Image.open('fact_image'+factualterm+".eps")
        image.save(Data_Flow_Player.saved_canvas+os.path.sep+"saved_images_fact_image"+factualterm+'.png','png')
        image.close()
        os.remove('fact_image'+factualterm+".eps")
        messagebox.showinfo("Information","Use Save for saving your interactions on the board in the lesson notes",parent=self)

    def open_image_window(self, image):
        # subprocess.run([title_image], check=False)
        if sys.platform == "win32":
            os.startfile(image)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, image])

    def add_factual_panel(self,labelframe,label, description, canvas, button,image,index):
        logger.info("Factual Page - add_factual_panel")
        labelframe.rowconfigure(0,weight=1)
        #labelframe.grid_columnconfigure(0, weight=1)

        labelframe.grid(row=0, column=0, padx=60, pady=0)
        self.image_frame = tk.Frame(labelframe)
        self.image_frame.configure(background='deepskyblue4')
        self.new_window_image_button = ttk.Button(self.image_frame, text="Zoom Image",
                                                  command=lambda: self.open_image_window(image),
                                                  style='Green.TButton')
        self.new_window_image_button.tooltip = tooltip.ToolTip(self.new_window_image_button, "Open in new window")
        self.image_save_button = ttk.Button(self.image_frame, text="Save Board",
                                            command=lambda: self.save_image_window(canvas,label.cget("text")),style='Green.TButton')
        self.image_save_button.tooltip = tooltip.ToolTip(self.image_save_button, "Save your additions to the Image.\n(will appear in lesson notes)")
        self.labeltext=label.cget("text")
        self.desctext=description.cget("text")
        self.text_zoom_button = ttk.Button(self.image_frame, text="Zoom Text",
                                            command=lambda: self.show_text_window(self.labeltext, self.desctext),
                                            style='Green.TButton')
        self.text_zoom_button.tooltip = tooltip.ToolTip(self.text_zoom_button, "View Text in larger size")
        self.text_zoom_button.grid(row=0, column=1, padx=10)
        self.new_window_image_button.grid(row=0,column=0,padx=10)
        self.image_save_button.grid(row=0,column=2,padx=10)



        self.forward_button = ttk.Button(labelframe, image =self.buttonnextimage,
                                            command=lambda:self.nextfact(index) ,
                                            style='Green.TButton')
        self.forward_button.tooltip = tooltip.ToolTip(self.forward_button, "Next")
        self.backward_button = ttk.Button(labelframe, image = self.buttonbackimage,
                                            command=lambda:self.move_previous_fact(index) ,
                                            style='Green.TButton')
        self.backward_button.tooltip = tooltip.ToolTip(self.backward_button, "Previous")
        if (index != 2):
            self.forward_button.grid(row=4,column=4,sticky=tk.S)

        label.grid(row=0,column=1,columnspan =2,sticky=tk.W)
        description.grid(row=1, column=1,columnspan=3,sticky=tk.W)
        self.image_frame.grid(row=2,column=1,columnspan=3,sticky=tk.NSEW)
        self.event_generate("<Configure>")
        canvas.grid(row=3, rowspan=3,column=1, columnspan=3, padx=150, pady=5, sticky=tk.NSEW)
        if (index != 0):
            self.backward_button.grid(row=4, column=0,sticky=tk.S)
        button.grid(row=5, column=0, padx = 5,sticky=tk.EW)




    def nextfact(self, index):
        logger.info("Factual Page - next fact")
        if index == 0:
            self.factual_index = 1
            self.labelframeone.grid_forget()

            self.add_factual_panel(self.labelframetwo, self.factual_term_label_two, self.factual_description_label_two,
                                   self.canvas_image2,
                                   self.voicebutton2, self.factual_image2,1)
        elif index == 1:
            self.factual_index = 2
            self.labelframetwo.grid_forget()

            self.add_factual_panel(self.labelframethree, self.factual_term_label_three,
                                   self.factual_description_label_three, self.canvas_image3,
                                   self.voicebutton3, self.factual_image3,2)







    def reset(self, event):
        self.old_x, self.old_y = None, None

    def paint(self, event, canvas):

        logger.info("Factual Page - paint")

        if self.old_x and self.old_y:
            canvas.create_line(self.old_x, self.old_y, event.x, event.y,
                                    width=5, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def   show_text_window(self,label,description):
      #  self.option_add('*Dialog.msg.font', 'Helvetica 30')
        logger.info("Factual Page - show_text_window")
        top = tk.Toplevel(self)
        top.configure(background="deepskyblue4")
        top.grab_set()
        top.transient(self)
        termlabel = ttk.Label(top,text=label,background='deepskyblue4',foreground='ivory2',wraplength=400,font=('courier', 32, 'bold', 'italic'))
        desclabel = ttk.Label(top,text=description, background='deepskyblue4', foreground='ivory2',wraplength=1000,font=('courier', 24, 'bold', 'italic'))
        closebutton = ttk.Button(top,text="Close",command=top.destroy,style="Green.TButton")

        voicebutton_top= ttk.Button(top, image=self.buttonimage,
                                   command=lambda: pageutils.playtextsound(description),
                                   style='Green.TButton')

        termlabel.pack()
        desclabel.pack()
        voicebutton_top.pack(side=tk.RIGHT)
        closebutton.pack()
       # self.option_clear()
    def move_previous_fact(self, index):
        logger.info("Factual Page - move_previous_fact")
        if index == 1:
            self.factual_index = 0
            self.labelframetwo.grid_forget()

            self.add_factual_panel(self.labelframeone, self.factual_term_label_one, self.factual_description_label_one,
                                   self.canvas_image1,
                                   self.voicebutton1, self.factual_image1,0)
            self.backward_button.grid_forget()
        elif index == 2:
            self.factual_index = 1
            self.labelframethree.grid_forget()
            self.add_factual_panel(self.labelframetwo, self.factual_term_label_two,
                                   self.factual_description_label_two, self.canvas_image2,
                                   self.voicebutton2, self.factual_image2,1)

    def playtextsound(self, text, v):
        logger.info("Factual Page - playtextsound")
        sound_speak = threading.Thread(target=pageutils.playtextsound, args=(text, v))
        sound_speak.start()


if __name__== "__main__":
        app = tk.Tk()
        app.geometry("600x600")
        app.screen_width = 600
        app.screen_height = 600
        frame = MagicFactualPage(app)

        frame.grid(row=0)
        app.mainloop()










