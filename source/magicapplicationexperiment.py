import os
import tkinter as tk
import random
from tkinter import ttk, font, filedialog, messagebox
import Data_Flow, configparser
from pathlib import Path

import  sys

from tkinter.colorchooser import askcolor

import PIL
from PIL import Image, ImageTk

import pageutils

_isLinux = sys.platform.startswith('linux')

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'
config = configparser.RawConfigParser()
two_up = Path(__file__).parents[2]
print(str(two_up)+'/magic.cfg')
db=config.read(str(two_up)+'/magic.cfg')
imageroot = config.get("section1",'image_root')

class MagicExperimentPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.config({'bg':'blue'})
        self.configure(background='dark slate gray')
        self.parent = parent
        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background='dark slate gray')
        s.configure('Red.TLabelframe.Label', font=('courier', 12, 'bold', 'italic'))
        s.configure('Red.TLabelframe.Label', foreground='PeachPuff2')
        s.configure('Red.TLabelframe.Label', background='dark slate gray')

        s.configure('Green.TButton', background='dark slate gray', foreground='PeachPuff2')
        s.configure('Horizontal.Green.TScale', background='dark slate gray', foreground='PeachPuff2')
        s.map('Green.TButton', background=[('active', '!disabled', 'dark olive green'), ('pressed', 'PeachPuff2')],
              foreground=[('pressed', 'PeachPuff2'), ('active', 'PeachPuff2')])
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0, weight=1)
        self.bind("<Configure>",self.resize_c)
        self.image_list = []
        self.image_canvas_list = []
        self.experiment_content_list = Data_Flow.get_experiment_content()
        self.experiment_content_terms = self.experiment_content_list[0]

        self.experiment_content_images = self.experiment_content_list[1]

        self.labelframeone = ttk.Labelframe(self, text="Let us do this !", relief=tk.RIDGE,style='Red.TLabelframe')
        self.labelframeone.grid_rowconfigure(1,weight=1)

        self.labelframetwo = ttk.Labelframe(self, text="Step by Step we can change the world !", relief=tk.RIDGE,style='Red.TLabelframe')
       # self.canvas_experiment = tk.Canvas(self.labelframeone,bg="white",width=parent.winfo_width()/1.5,height=parent.winfo_height()/1.5)

        self.canvas_experiment = tk.Canvas(self.labelframeone, bg="white")


        self.labelframeone.grid(row=0, pady=5, padx = 20)
        self.labelframetwo.grid(row=1, pady= 5, padx = 20)
        self.sound_flag = True

        self.fill_steps_frame(parent.screen_width,parent.screen_height)
        self.fill_canvas_frame(parent.screen_width,parent.screen_height)

    def resize_c(self,event):
        print("frame resized"+str(self.winfo_width()))

        self.canvas_experiment.configure(width=self.winfo_width()/1.2 ,
                                    height=self.winfo_height() / 2)


    def save_image_window(self,canvas,factualterm):
        # subprocess.run([title_image], check=False)
        canvas.postscript(file='apply_image'+str(factualterm)+".eps")
        image = Image.open('apply_image'+str(factualterm)+".eps")
        image.save(imageroot+'saved_images/apply_image'+str(factualterm)+'.png','png')
        image.close()
        os.remove('apply_image'+str(factualterm)+".eps")
        messagebox.showinfo("Information","Image saved under saved_images folder")


    def fill_steps_frame(self,width,height):

         self.index = 1
         self.step_one_label = ttk.Label(self.labelframetwo, text="Step 1", foreground='ivory2',
                                         font=("TkCaptionFont", 14), background='dark slate gray')
         self.step_one_desc_label = ttk.Label(self.labelframetwo, text = self.experiment_content_terms[0],foreground = 'PeachPuff2',wraplength=450, font=("TkCaptionFont", 12,font.ITALIC),background='dark slate gray')

         self.stepbutton = ttk.Button(self.labelframetwo, text= "Next Step",style='Green.TButton')
         self.step_one_label.grid(row=1, column=0)
         self.step_one_desc_label.grid(row=1, column=1,columnspan=2,sticky=tk.W, padx = 50)
         self.stepbutton.grid(row=0, column = 0, sticky=tk.NW)

         imagefile = self.experiment_content_images[0]
         imageid = self.draw_image(imagefile, 100, 100)
         self.audiobutton = ttk.Button(self.labelframetwo, text="Voice-On", style='Green.TButton',command= self.play_step_audio)

         self.audiooffbutton = ttk.Button(self.labelframetwo, text="Voice-Off", style='Green.TButton',
                                  command= self.stop_step_audio)
         self.audiobutton.grid(row =0,padx = 20,column=1,sticky=tk.NW)
         self.audiooffbutton.grid(row=0, column=3, sticky=tk.NW)

         self.stepbutton.configure(command=lambda: self.addnewstep(width, height))

    def play_step_audio(self):
        self.sound_flag = True
    def stop_step_audio(self):
        self.sound_flag = False

    def move_animate(self, canvas,imageid, finalx, finaly):
        x, y = canvas.coords(imageid)
        if x >= finalx:
            xmove = 0
        else:
            xmove = 5
        if y >=finaly:
            ymove = 0
        else:
            ymove = 5

        canvas.move(imageid, xmove, ymove)

        print(str(x)+","+str(y))
        if x >= finalx and y >= finaly:
            return
        self.labelframeone.after(50,lambda: self.move_animate(canvas,imageid,finalx,finaly))
    def fill_canvas_frame(self,width,height):
        self.image_button = ttk.Button(self.labelframeone, text='Add Image', command=self.use_image,style='Green.TButton')
        self.image_button.grid(row=0, column=0,padx=5)

        self.image_act_button = ttk.Button(self.labelframeone, text='Move Image', command=self.use_image_act,style='Green.TButton')
        self.image_act_button.grid(row=0, column=1,padx=5)

        self.pen_button = ttk.Button(self.labelframeone, text='Pen', command=self.use_pen,style='Green.TButton')
        self.pen_button.grid(row=0, column=2,padx=5)


        self.color_button = ttk.Button(self.labelframeone, text='Color', command=self.choose_color,style='Green.TButton')
        self.color_button.grid(row=0, column=3,padx=5)

        self.eraser_button = ttk.Button(self.labelframeone, text='Eraser', command=self.use_eraser,style='Green.TButton')
        self.eraser_button.grid(row=0, column=4,padx=5)
        device = config.get("section1", 'device_type')
        self.choose_size_button = tk.Scale(self.labelframeone, orient=tk.HORIZONTAL, from_=1, to=10,
                                           background='dark slate gray', foreground='PeachPuff2')
        self.clear_button = ttk.Button(self.labelframeone, text='Clear', command=self.clear, style='Green.TButton')
        self.buttonimage = tk.PhotoImage(file="../images/save.png")
        self.image_save_button = ttk.Button(self.labelframeone, text="Save Canvas",image=self.buttonimage,
                                            command=lambda: self.save_image_window(self.canvas_experiment, random.randint(0,100)),
                                            style='Green.TButton')

        if (device == 'laptop'):
             self.choose_size_button.grid(row=0, column=5,padx=5)
             self.clear_button.grid(row=0, column=6)

        self.canvas_experiment.grid(row=1, pady=5, padx=20, columnspan = 7)
        self.image_save_button.grid(row=1,column=8,sticky=tk.N)

        self.setup_canvas()


    def use_image(self):
        self.activate_button(self.image_button)
        self.canvas_experiment.bind('<B1-Motion>', "")
        self.canvas_experiment.bind('<ButtonRelease-1>', "")
       # tk.Tk().withdraw()  # avoids window accompanying tkinter FileChooser
        img = filedialog.askopenfilename(initialdir=imageroot, title="Select image file",
                                         filetypes=(
                                             ("jpeg files", "*.jpg"), ("png files", "*.png"), ("gif files", "*.gif")))
        self.draw_image(img,self.canvas_experiment.winfo_width()-100,self.canvas_experiment.winfo_height()-100)

        self.move_flag = False
    def draw_image(self, imagefile,xpos, ypos):
      try:
            image1 = Image.open(imagefile)

            image1.thumbnail((200, 200))
            fimage1_display = ImageTk.PhotoImage(image1)
            self.image_list.append(fimage1_display)
            image1_id = self.canvas_experiment.create_image(xpos, ypos, image=self.image_list[len(self.image_list) - 1],
                                                            tags="D")
            self.image_canvas_list.append(image1_id)
            self.canvas_experiment.tag_bind(self.image_canvas_list[len(self.image_canvas_list) - 1], "<Button1-Motion>",
                                            self.move)
            self.canvas_experiment.tag_bind(self.image_canvas_list[len(self.image_canvas_list) - 1], "<ButtonRelease-1>",self.release)
            return image1_id
      except (FileNotFoundError, IsADirectoryError):
            messagebox.showwarning("Warning", "Step Images could not be retrieved \n")
            return None






    def use_image_act(self):
        self.activate_button(self.image_act_button)
        self.canvas_experiment.bind('<B1-Motion>', "")
        self.canvas_experiment.bind('<ButtonRelease-1>', "")
        for image in self.image_canvas_list:
            self.canvas_experiment.tag_bind(image, "<Button1-Motion>", self.move)
            self.canvas_experiment.tag_bind(image, "<ButtonRelease-1>", self.release)

    def move(self, event):
        print("move")
        item = self.canvas_experiment.find_closest(event.x, event.y)
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y

            if  'D' in self.canvas_experiment.gettags(item):
                self.canvas_experiment.move(item,
                             new_xpos - self.mouse_xpos, new_ypos - self.mouse_ypos)

                self.mouse_xpos = new_xpos
                self.mouse_ypos = new_ypos
        else:

            if 'D' in self.canvas_experiment.gettags(item):
                self.move_flag = True
                self.canvas_experiment.tag_raise(item)
                self.mouse_xpos = event.x
                self.mouse_ypos = event.y

    def release(self, event):
        self.move_flag = False






    def use_pen(self):
        self.canvas_experiment.bind('<B1-Motion>', self.paint)
        self.canvas_experiment.bind('<ButtonRelease-1>', self.reset)
        self.line_width = self.choose_size_button.get()
        self.activate_button(self.pen_button)

    def select_image(self,event):
        item = self.canvas_experiment.find_closest(event.x, event.y)
        if "D" in self.canvas_experiment.getTags(item):
            self.canvas_experiment.addtag_below("S",item)
        self.canvas_experiment.create_rectangle(event.x-50,event.y-50,event)



    def choose_color(self):
        self.eraser_on = False
        self.line_width = self.choose_size_button.get()
        self.color = askcolor(color=self.color)[1]
    def use_eraser(self):
        self.canvas_experiment.bind('<B1-Motion>', self.paint)
        self.canvas_experiment.bind('<ButtonRelease-1>', self.reset)

        self.activate_button(self.eraser_button, eraser_mode=True)

    def clear(self):
        self.canvas_experiment.bind('<B1-Motion>', "")
        self.canvas_experiment.bind('<ButtonRelease-1>', "")
        self.canvas_experiment.delete("all")

    def setup_canvas(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button


    def activate_button(self, some_button, eraser_mode=False):
        #self.active_button.config(relief=tk.RAISED)
        #some_button.config(relief=tk.SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        item = self.canvas_experiment.find_closest(event.x, event.y)
        self.canvas_experiment.tag_unbind(item, "<Button1-Motion>")
        self.canvas_experiment.tag_unbind(item, "<ButtonRelease-1>")

        #self.line_width = self.choose_size_button.get()
        if self.eraser_on:
            paint_color = 'white'
            self.line_width = 20
        else:
            paint_color = self.color
            self.line_width = self.choose_size_button.get()


        if self.old_x and self.old_y:
            self.canvas_experiment.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None



    def addnewstep(self,width,height):
        self.step_labels = []
        self.step_descriptions = []
        if self.index < self.experiment_content_list[2]:
            label = ttk.Label(self.labelframetwo, text="Step "+str(self.index+1), foreground='ivory2',
                                            font=("TkCaptionFont", 14),background='dark slate gray')
            desc_label = ttk.Label(self.labelframetwo, text=self.experiment_content_terms[self.index],
                                                 foreground='PeachPuff2', font=("TkCaptionFont", 12,font.ITALIC),background='dark slate gray')
            label.grid(row=self.index+1, column=0)
            desc_label.grid(row=self.index+1, column=1,sticky=tk.W, padx = 50)
            self.step_labels.append(label)
            self.step_descriptions.append(desc_label)
            imagefile = self.experiment_content_images[self.index]
            imageid = self.draw_image(imagefile,100, 100)
            self.move_animate(self.canvas_experiment, imageid, self.canvas_experiment.winfo_width()-100,self.canvas_experiment.winfo_height()-100)
            self.move_flag = False
            if self.sound_flag:
                 pageutils.playtextsound(self.experiment_content_terms[self.index])


        self.index += 1


if __name__== "__main__":
        app = tk.Tk()
        app.geometry("600x600")
        frame = MagicExperimentPage(app)

        frame.grid(row=0)
        app.mainloop()










