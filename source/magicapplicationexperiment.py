import tkinter as tk
from tkinter import ttk, font, filedialog
import Data_Flow
import pyttsx3
import vlc, sys, time
import unicodedata
import scroll_bars
from tkinter.colorchooser import askcolor

import PIL
from PIL import Image, ImageTk

import pageutils

_isLinux = sys.platform.startswith('linux')

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'

class MagicExperimentPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.config({'bg':'blue'})
        self.image_list = []
        self.image_canvas_list = []
        self.experiment_content_list = Data_Flow.get_experiment_content()
        self.experiment_content_terms = self.experiment_content_list[0]
        print(self.experiment_content_terms)
        self.experiment_content_images = self.experiment_content_list[1]
        print(self.experiment_content_images)
        self.labelframeone = ttk.Labelframe(self, width = 1200, height = 500, text="Let us do this !", relief=tk.RIDGE)
        self.labelframetwo = ttk.Labelframe(self, width = 1200, height = 300,text="Step by Step we can change the world !", relief=tk.RIDGE)
        self.canvas_experiment = tk.Canvas(self.labelframeone,
                                       width=1000,
                                       height=400,bg="white")
        self.labelframeone.grid_propagate(False)
        self.labelframetwo.grid_propagate(False)
        self.labelframeone.grid(row=0, pady=40, padx = 20)
        self.labelframetwo.grid(row=1, pady= 40, padx = 20)

        self.fill_steps_frame()
        self.fill_canvas_frame()


    def fill_steps_frame(self):
         self.index = 1
         self.step_one_label = ttk.Label(self.labelframetwo, text="Step 1", foreground='brown',
                                         font=("TkCaptionFont", 14))
         self.step_one_desc_label = ttk.Label(self.labelframetwo, text = self.experiment_content_terms[0],foreground = 'blue', font=("TkCaptionFont", 12,font.ITALIC))

         self.stepbutton = ttk.Button(self.labelframetwo, text= "Next Step")
         self.step_one_label.grid(row=1, column=0)
         self.step_one_desc_label.grid(row=1, column=1,sticky=tk.W, padx = 50)
         self.stepbutton.grid(row=0, column = 0, sticky=tk.NW)
         self.stepbutton.configure(command=self.addnewstep)
         imagefile = "../images/" + self.experiment_content_images[0]
         imageid = self.draw_image(imagefile, 950, 300)


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
    def fill_canvas_frame(self):
        self.image_button = tk.Button(self.labelframeone, text='Add New Image', command=self.use_image)
        self.image_button.grid(row=0, column=0)

        self.image_act_button = tk.Button(self.labelframeone, text='Images Activate', command=self.use_image_act)
        self.image_act_button.grid(row=0, column=1)

        self.pen_button = tk.Button(self.labelframeone, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=2)


        self.color_button = tk.Button(self.labelframeone, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=3)

        self.eraser_button = tk.Button(self.labelframeone, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=4)

        self.choose_size_button = tk.Scale(self.labelframeone,orient=tk.HORIZONTAL, from_=1,to=10)
        self.choose_size_button.grid(row=0, column=5)
        self.clear_button = tk.Button(self.labelframeone, text='Clear', command=self.clear)
        self.clear_button.grid(row=0, column=6)


        self.canvas_experiment.grid(row=1, pady=20, padx=40, columnspan = 7)
        self.setup_canvas()


    def use_image(self):
        self.activate_button(self.image_button)
        self.canvas_experiment.bind('<B1-Motion>', "")
        self.canvas_experiment.bind('<ButtonRelease-1>', "")
       # tk.Tk().withdraw()  # avoids window accompanying tkinter FileChooser
        img = filedialog.askopenfilename(initialdir="../images", title="Select image file",
                                         filetypes=(
                                             ("jpeg files", "*.jpg"), ("png files", "*.png"), ("gif files", "*.gif")))
        self.draw_image(img,300,200)

        self.move_flag = False
    def draw_image(self, imagefile,xpos, ypos):
        image1 = Image.open(imagefile)
        image1.thumbnail((50, 50))
        fimage1_display = ImageTk.PhotoImage(image1)
        self.image_list.append(fimage1_display)
        image1_id = self.canvas_experiment.create_image(xpos, ypos, image=self.image_list[len(self.image_list) - 1],
                                                        tags="D")
        self.image_canvas_list.append(image1_id)
        self.canvas_experiment.tag_bind(self.image_canvas_list[len(self.image_canvas_list) - 1], "<Button1-Motion>",
                                        self.move)
        self.canvas_experiment.tag_bind(self.image_canvas_list[len(self.image_canvas_list) - 1], "<ButtonRelease-1>",
                                        self.release)
        return image1_id

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
        self.active_button.config(relief=tk.RAISED)
        some_button.config(relief=tk.SUNKEN)
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



    def addnewstep(self):
        self.step_labels = []
        self.step_descriptions = []
        if self.index < self.experiment_content_list[2]:
            label = ttk.Label(self.labelframetwo, text="Step"+str(self.index+1), foreground='brown',
                                            font=("TkCaptionFont", 14))
            desc_label = ttk.Label(self.labelframetwo, text=self.experiment_content_terms[self.index],
                                                 foreground='blue', font=("TkCaptionFont", 12,font.ITALIC))
            label.grid(row=self.index+1, column=0)
            desc_label.grid(row=self.index+1, column=1,sticky=tk.W, padx = 50)
            self.step_labels.append(label)
            self.step_descriptions.append(desc_label)
            imagefile = "../images/"+self.experiment_content_images[self.index]
            imageid = self.draw_image(imagefile,50, 50)
            self.move_animate(self.canvas_experiment, imageid, 900, 300)
            self.move_flag = False


        self.index += 1


if __name__== "__main__":
        app = tk.Tk()
        app.geometry("600x600")
        frame = MagicExperimentPage(app)

        frame.grid(row=0)
        app.mainloop()










