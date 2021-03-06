import logging
import os
import random
import threading
import time
import traceback

import sys
import cv2
import tkinter as tk
import webbrowser
from tkinter import ttk, font, filedialog, messagebox, simpledialog
from tkinter.colorchooser import askcolor

import pyautogui
from PIL import Image, ImageTk

import Data_Flow_Player
import pageutils
import tooltip

_isLinux = sys.platform.startswith('linux')

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'

logger = logging.getLogger("MagicLogger")
class MagicExperimentPage(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #self.config({'bg':'blue'})
        logger.info("Inside MagicExperimentPage Initialize")
        self.configure(background='deepskyblue4')
        self.parent = parent
        s = ttk.Style(self)
        self.unbind_all('<Control-Key-z>')
        self.unbind_all('<Control-Key-s>')
        self.unbind_all('<Control-Key-x>')


        s.configure('Horizontal.Green.TScale', background='deepskyblue4', foreground='white')



        self.move_animation_Steps = 12
        self.move_flag=False
        self.rowconfigure(0,weight=1)
        self.columnconfigure(1, weight=1)
        self.bind("<Configure>",self.resize_c)
        self.image_list = []
        self.image_canvas_list = []
        self.experiment_content_list = Data_Flow_Player.get_experiment_content()
        self.experiment_content_terms = self.experiment_content_list[0]
        self.image_map = {}

        self.experiment_content_images = self.experiment_content_list[1]

        self.labelframeone = ttk.Labelframe(self, text="Let us do this !", relief=tk.RIDGE,style='Red.TLabelframe')
        self.labelframeone.grid_rowconfigure(1,weight=1)

        self.labelframetwo = ttk.Labelframe(self, text="Step by Step we can change the world !", relief=tk.RIDGE,style='Red.TLabelframe')
       # self.canvas_experiment = tk.Canvas(self.labelframeone,bg="white",width=parent.winfo_width()/1.5,height=parent.winfo_height()/1.5)

        self.canvas_experiment = tk.Canvas(self.labelframeone, bg="white")
        self.popup_menu = tk.Menu(self.canvas_experiment, background='deepskyblue4', foreground='white',tearoff=0)
        self.popup_menu.add_command(label="Text")
        self.popup_menu.add_command(label="Move Down")
        self.popup_menu.add_command(label="Move Right")
        self.popup_menu.add_command(label="Zoom")
        self.canvas_experiment.bind('<Button-3>', self.show_popup_menu)


        self.labelframeone.grid(row=0,column=1, pady=5, padx = 20)
        self.labelframetwo.grid(row=0,column=0, pady= 10, padx = 20,sticky=tk.N)
        self.sound_flag = True

        self.fill_steps_frame(parent.screen_width,parent.screen_height)
        self.fill_canvas_frame(parent.screen_width,parent.screen_height)
        link_ext = Data_Flow_Player.get_link()
        if(link_ext is not None and link_ext != ""):
            self.link_button = ttk.Button(self.labelframetwo,text="Launch Link",command=lambda: self.launch_link(link_ext),style="Green.TButton")
            self.link_button.tooltip = tooltip.ToolTip(self.link_button, "Opens Browser")
            self.link_button.grid(row=10, column=2,sticky=tk.SW,padx=10)


    def launch_link(self,link):
        webbrowser.open(link,new=2)

    def zoom_image(self,event,canvas):
        logger.info("Experiment Page - Zoom_image")
        item = canvas.find_closest(event.x, event.y)
        if 'D' in canvas.gettags(item):
            self.image_canvas_list.remove(item[0])
            canvas.delete(item)

            image = self.image_map.get(item[0])
            image_id = self.draw_image(image,event.x,event.y,250,250)
            self.image_map[image_id] = image




    def show_popup_menu(self, event):
        logger.info("Experiment Page - pop_up_menu")
        self.popup_menu.tk_popup(event.x_root, event.y_root)
        self.popup_menu.entryconfig("Move Down",command=lambda:self.move_vertical(event,0))
        self.popup_menu.entryconfig("Move Right", command=lambda: self.move_horizontal(event,0))
        self.popup_menu.entryconfig("Zoom", command=lambda: self.zoom_image(event, self.canvas_experiment))
        self.popup_menu.entryconfig("Text", command=lambda: self.paint_text(event, self.canvas_experiment))
    def paint_text(self, event,canvas):
        logger.info("Experiment Page - paint_Text")
        answer = simpledialog.askstring("Text to add", "Add text to the location",
                                        parent=self.parent)
        if answer is not None:
            canvas.create_text(event.x, event.y, font=("comic sans", 22, "bold"), text=answer, fill=self.color)
    def resize_c(self,event):
        print("frame resized"+str(self.winfo_width()))

        self.canvas_experiment.configure(width=self.winfo_width()/1.7 ,
                                    height=self.winfo_height() / 1.2)


    def save_image_window(self,canvas,factualterm):
        # subprocess.run([title_image], check=False)
        logger.info("Experiment Page - save_image_window")
        try:
            image = pyautogui.screenshot(Data_Flow_Player.saved_canvas+os.path.sep+'skill_board'+str(factualterm)+'.png')
            messagebox.showinfo("Save Board", "Board saved into the lesson notes", parent=self)
        except:
            logger.exception("Canvas Image Could Not be Saved")



    def fill_steps_frame(self,width,height):
         logger.info("Experiment Page - fill_steps_frame")
         self.index = 1
         self.step_one_label = ttk.Label(self.labelframetwo, text="1", foreground='white',
                                         font=("helvetica", 14,'bold'), background='deepskyblue4')
         self.step_one_desc_label = ttk.Label(self.labelframetwo, text = self.experiment_content_terms[0],foreground = 'white',wraplength=250, font=("helvetica", 14,'bold'),background='deepskyblue4')

         self.stepbutton = ttk.Button(self.labelframetwo, text= "Next Step",style='Green.TButton')
         self.stepbutton.tooltip = tooltip.ToolTip(self.stepbutton, "Next Step\nctrl-n")
         self.step_one_label.grid(row=1, column=0)
         self.step_one_desc_label.grid(row=1, column=1,sticky=tk.W,columnspan=2, padx = 50)
         self.stepbutton.grid(row=0, column = 0,pady=5, sticky=tk.NW,padx=5)
         sound_speak1 = threading.Thread(target=pageutils.playtextsound,
                                        args=(self.experiment_content_terms[0], 'f'))
         sound_speak1.start()

         imagefile = self.experiment_content_images[0]
         imageid = self.draw_image(imagefile, 100, 100,150,150)
         if imageid != None:
             self.image_map[imageid] = imagefile
         self.audiobutton = ttk.Button(self.labelframetwo, text="Voice-On", style='Green.TButton',command= self.play_step_audio)

         self.audiooffbutton = ttk.Button(self.labelframetwo, text="Voice-Off", style='Green.TButton',
                                      command= self.stop_step_audio)
         self.audiobutton.grid(row =0,padx = 20,column=1,sticky=tk.NW,pady=5)
         self.audiooffbutton.grid(row=0, column=2, sticky=tk.NW,pady=5)
         self.stepbutton.configure(command=lambda: self.addnewstep(width, height))
         self.bind_all('<Control-Key-n>',lambda event,w=width,h=height:self.addnewstep(w,h,event))


    def play_step_audio(self):
        self.sound_flag = True
    def stop_step_audio(self):
        self.sound_flag = False

    def move_animate(self, canvas,imageid, finalx, finaly):
        logger.info("Experiment Page - move_animate")
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
        logger.info("Experiment Page - fill_canvas_frame")
        self.button_frame= tk.Frame(self.labelframeone,background="deepskyblue4")
        self.add_image_icon = tk.PhotoImage(file="../images/image_open.png")
        self.add_camera_icon = tk.PhotoImage(file="../images/camera.png")
        self.image_button = ttk.Button(self.button_frame, text='Add Image',image=self.add_image_icon, command=self.use_image,style='Green.TButton')
        self.image_button.grid(row=0, column=0,padx=5)
        self.image_button.tooltip = tooltip.ToolTip(self.image_button, "Open an image file")
        self.camera_button = ttk.Button(self.button_frame, text='Add Image', image=self.add_camera_icon,
                                       command=self.use_camera, style='Green.TButton')
        self.camera_button.grid(row=0, column=1, padx=5)
        self.camera_button.tooltip = tooltip.ToolTip(self.camera_button, "Capture from Camera")

        self.move_image_icon = tk.PhotoImage(file="../images/image_move.png")
        self.image_act_button = ttk.Button(self.button_frame, text='Move Image', image = self.move_image_icon,command=self.use_image_act,style='Green.TButton')
        self.image_act_button.grid(row=0, column=2,padx=5)
        self.image_act_button.tooltip = tooltip.ToolTip(self.image_act_button, "Enable Moving of Images")

        self.pen_image_icon = tk.PhotoImage(file="../images/pen_brush.png")
        self.pen_button = ttk.Button(self.button_frame, text='Pen',image = self.pen_image_icon, command=self.use_pen,style='Green.TButton')
        self.pen_button.grid(row=0, column=3,padx=5)
        self.pen_button.tooltip = tooltip.ToolTip(self.pen_button, "Draw with a Pen")

        self.color_image_icon = tk.PhotoImage(file="../images/color_pal.png")
        self.color_button = ttk.Button(self.button_frame, text='Color', image= self.color_image_icon,command=self.choose_color,style='Green.TButton')
        self.color_button.grid(row=0, column=4,padx=5)
        self.color_button.tooltip = tooltip.ToolTip(self.color_button, "Choose a Color")

        self.eraser_image_icon = tk.PhotoImage(file="../images/erase.png")
        self.eraser_button = ttk.Button(self.button_frame, text='Eraser',image=self.eraser_image_icon, command=self.use_eraser,style='Green.TButton')
        self.eraser_button.grid(row=0, column=5,padx=5)
        self.eraser_button.tooltip = tooltip.ToolTip(self.eraser_button, "Erase Drawing")

        self.choose_size_button = tk.Scale(self.button_frame, orient=tk.HORIZONTAL, from_=1, to=10,
                                           background='deepskyblue4', foreground='white')
        self.choose_size_button.set(5)
        self.choose_size_button.tooltip = tooltip.ToolTip(self.choose_size_button, "Line Size of the Pen")

        self.clear_image_icon = tk.PhotoImage(file="../images/cls.png")
        self.clear_button = ttk.Button(self.button_frame, text='Clear', image=self.clear_image_icon,command=self.clear, style='Green.TButton')
        self.clear_button.tooltip = tooltip.ToolTip(self.clear_button, "Clear Entire Canvas")

        self.buttonimage = tk.PhotoImage(file="../images/save.png")

        self.image_save_button = ttk.Button(self.button_frame, text="Save Canvas",image=self.buttonimage,
                                            command=lambda: self.save_image_window(self.canvas_experiment, random.randint(0,100)),
                                            style='Green.TButton')

        self.image_save_button.tooltip = tooltip.ToolTip(self.image_save_button, "Save Canvas to view in Lesson Notes")


        self.choose_size_button.grid(row=0, column=6,padx=5)
        self.clear_button.grid(row=0, column=7,padx=5)
        self.button_frame.grid(row=0,column=0,columnspan=7,pady=8)
        self.canvas_experiment.grid(row=1, pady=5, padx=20, columnspan = 7)
        self.image_save_button.grid(row=0,column=8,sticky=tk.N)

        self.setup_canvas()


    def use_image(self):
        logger.info("Experiment Page - use_image")
        self.activate_button(self.camera_button)
        self.canvas_experiment.bind('<B1-Motion>', "")
        self.canvas_experiment.bind('<ButtonRelease-1>', "")
       # tk.Tk().withdraw()  # avoids window accompanying tkinter FileChooser
        img = filedialog.askopenfilename(initialdir=Data_Flow_Player.file_root, parent=self,title="Select image file",
                                         filetypes=(
                                             ("jpeg files", "*.jpg"), ("png files", "*.png"), ("gif files", "*.gif")))
        imageid = self.draw_image(img,self.canvas_experiment.winfo_width()-100,self.canvas_experiment.winfo_height()-100,150,150)
        self.image_map[imageid] = img

        self.move_flag = False
    def use_camera(self):
        logger.info("Experiment Page - use_camera")
        messagebox.showinfo("Camera Info","Camera will now open.\nPress the key 's' to capture image\nPress 'esc'"
                                          "to close the camera",parent=self)
        self.activate_button(self.image_button)
        self.canvas_experiment.bind('<B1-Motion>', "")
        self.canvas_experiment.bind('<ButtonRelease-1>', "")
        # tk.Tk().withdraw()  # avoids window accompanying tkinter FileChooser
        self.capture_view()
        #capture_cam = threading.Thread(target= self.capture_view)
        #capture_cam.start()
        #capture_cam.join()
        imageid = self.draw_image("savedone.png", self.canvas_experiment.winfo_width() - 100,
                                  self.canvas_experiment.winfo_height() - 100, 150, 150)
        self.image_map[imageid] = "savedone.png"

        self.move_flag = False

    def capture_view(self):
        if os.path.exists("savedone.png"):
            os.remove("savedone.png")
        save_image = cv2.VideoCapture(0)

        while (True):

            # Capture the video frame
            # by frame
            ret, frame = save_image.read()
            if not ret:
                print("failed to grab frame")
                break
            # Display the resulting frame
            cv2.imshow('Take a Pic', frame)

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            k=cv2.waitKey(1)
            if k == 27:
               # cv2.imwrite("savedone.p ng", frame)
                break
            if k == ord('s'):

                cv2.imwrite("savedone.png",frame)
                break
            if cv2.getWindowProperty('Take a Pic', cv2.WND_PROP_VISIBLE) < 1:
                break

        save_image.release()
        cv2.destroyAllWindows()

    def draw_image(self, imagefile,xpos, ypos,scale1,scale2):
      logger.info("Experiment Page - draw_image")
      try:
            image1 = Image.open(imagefile)

            image1.thumbnail((scale1, scale2))
            fimage1_display = ImageTk.PhotoImage(image1)
            self.image_list.append(fimage1_display)
            self.image1_id = self.canvas_experiment.create_image(xpos, ypos, image=self.image_list[len(self.image_list) - 1],
                                                            tags="D")
            self.image_canvas_list.append(self.image1_id)
            self.canvas_experiment.tag_bind(self.image_canvas_list[len(self.image_canvas_list) - 1], "<Button1-Motion>",
                                            self.move)
            self.canvas_experiment.tag_bind(self.image_canvas_list[len(self.image_canvas_list) - 1], "<ButtonRelease-1>",self.release)
            return self.image1_id
      except (FileNotFoundError, IsADirectoryError):
            #messagebox.showwarning("Warning", "Step Images could not be retrieved \n",parent=self)
            logger.exception("Step Images could not be retrieved")
            return None





    def use_image_act(self):
        logger.info("Experiment Page - use_image_act")
        self.activate_button(self.image_act_button)
        self.canvas_experiment.bind('<B1-Motion>', "")
        self.canvas_experiment.bind('<ButtonRelease-1>', "")
        for image in self.image_canvas_list:
            self.canvas_experiment.tag_bind(image, "<Button1-Motion>", self.move)
            self.canvas_experiment.tag_bind(image, "<ButtonRelease-1>", self.release)

    def move_horizontal(self,event,index):
        logger.info("Experiment Page - move_horizontal")
        item = self.canvas_experiment.find_closest(event.x, event.y)
        if 'D' in self.canvas_experiment.gettags(item):
            self.move_in_X(item,index,self.canvas_experiment)

    def move_in_X(self,item,index,canvas):
        logger.info("Experiment Page - move_in_X")
        canvas.move(item, 30, 0)
        X, Y = canvas.coords(item)
        index += 1
        if index == self.move_animation_Steps or X >= canvas.winfo_width()-100:
            return
        else:
            self.canvas_experiment.after(500, self.move_in_X,item,index,canvas)

    def move_in_Y(self,item,index,canvas):
        logger.info("Experiment Page - move_in_Y")
        canvas.move(item, 0, 30)
        X,Y = canvas.coords(item)
        index += 1
        if index == self.move_animation_Steps or Y >=canvas.winfo_height()-100:
            return
        else:
            self.canvas_experiment.after(500, self.move_in_Y,item,index,canvas)

    def move_vertical(self,event,index):
        logger.info("Experiment Page - move_vertical")
        item = self.canvas_experiment.find_closest(event.x, event.y)
        if 'D' in self.canvas_experiment.gettags(item):
            self.move_in_Y(item, index, self.canvas_experiment)


    def move(self, event):
        logger.info("Experiment Page - move")
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
        logger.info("Experiment Page - use_pen")
        for image in self.image_canvas_list:
            self.canvas_experiment.tag_unbind(image, "<Button1-Motion>")
            self.canvas_experiment.tag_unbind(image, "<ButtonRelease-1>")
        self.canvas_experiment.bind('<B1-Motion>', self.paint)
        self.canvas_experiment.bind('<ButtonRelease-1>', self.reset)
        self.line_width = self.choose_size_button.get()
        self.activate_button(self.pen_button)

    def select_image(self,event):
        logger.info("Experiment Page - select_image")
        item = self.canvas_experiment.find_closest(event.x, event.y)
        if "D" in self.canvas_experiment.getTags(item):
            self.canvas_experiment.addtag_below("S",item)
        self.canvas_experiment.create_rectangle(event.x-50,event.y-50,event)



    def choose_color(self):
        logger.info("Experiment Page - choose_color")
        self.eraser_on = False
        self.line_width = self.choose_size_button.get()
        self.color = askcolor(color=self.color,parent=self)[1]
        self.use_pen()
    def use_eraser(self):
        logger.info("Experiment Page - use_eraser")
        self.canvas_experiment.bind('<B1-Motion>', self.paint)
        self.canvas_experiment.bind('<ButtonRelease-1>', self.reset)

        self.activate_button(self.eraser_button, eraser_mode=True)

    def clear(self):
        logger.info("Experiment Page - clear")
        self.canvas_experiment.bind('<B1-Motion>', "")
        self.canvas_experiment.bind('<ButtonRelease-1>', "")
        self.canvas_experiment.delete("all")
        self.image_canvas_list.clear()
        self.image_map.clear()

    def setup_canvas(self):
        logger.info("Experiment Page - setup_canvas")
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button


    def activate_button(self, some_button, eraser_mode=False):
        logger.info("Experiment Page - activate_button")
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        logger.info("Experiment Page - paint")
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
                               capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=56)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None



    def addnewstep(self,width,height,event=None):
        logger.info("Experiment Page - addnewstep")
        self.step_labels = []
        self.step_descriptions = []
        if self.index < self.experiment_content_list[2]:
            label = ttk.Label(self.labelframetwo, text=str(self.index+1), foreground='white',
                                            font=("helvetica", 14,'bold'),background='deepskyblue4')
            desc_label = ttk.Label(self.labelframetwo, text=self.experiment_content_terms[self.index],wraplength=250,
                                                 foreground='white', font=("helvetica", 14,'bold'),background='deepskyblue4')
            label.grid(row=self.index+1, column=0)
            desc_label.grid(row=self.index+1, column=1,sticky=tk.W,columnspan=2, padx = 50)
            self.step_labels.append(label)
            self.step_descriptions.append(desc_label)
            imagefile = self.experiment_content_images[self.index]
            imageid = self.draw_image(imagefile,100, 100,150,150)

            if imageid != None:
                self.image_map[imageid] = imagefile
                self.move_animate(self.canvas_experiment, imageid, self.canvas_experiment.winfo_width()-self.index*100,self.canvas_experiment.winfo_height()-100)
                self.move_flag = False
            if self.sound_flag:
                sound_speak = threading.Thread(target=pageutils.playtextsound, args=(self.experiment_content_terms[self.index], 'f'))
                sound_speak.start()



        self.index += 1


if __name__== "__main__":
        app = tk.Tk()
        app.geometry("600x600")
        frame = MagicExperimentPage(app)

        frame.grid(row=0)
        app.mainloop()










