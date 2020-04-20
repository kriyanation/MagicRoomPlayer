import os
import tkinter as tk
from tkinter import ttk, StringVar, messagebox, Scrollbar
import Data_Flow,configparser
from pathlib import Path
import  sys
from multiprocessing import Process


import cv2
import time

import cv2practice
import pageutils


_isLinux = sys.platform.startswith('linux')

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'

config = configparser.RawConfigParser()
two_up = Path(__file__).resolve().parents[2]
print(str(two_up)+'/magic.cfg')
config.read(str(two_up)+'/magic.cfg')
imageroot = config.get("section1",'image_root')

class MagicIndenpendentPractice(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.configure(background='dark slate gray')
        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background='dark slate gray')
        s.configure('Red.TLabelframe.Label', font=('courier', 12, 'bold', 'italic'))
        s.configure('Red.TLabelframe.Label', foreground='PeachPuff2')
        s.configure('Red.TLabelframe.Label', background='dark slate gray')

        s.configure('Green.TButton', background='dark slate gray', foreground='PeachPuff2')
        s.configure('Horizontal.Green.TScale', background='dark slate gray', foreground='PeachPuff2')
        s.map('Green.TButton', background=[('active', '!disabled', 'dark olive green'), ('pressed', 'PeachPuff2')],
              foreground=[('pressed', 'PeachPuff2'), ('active', 'PeachPuff2')])

        self.cameraoff = False
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.panel = None
        self.status_text = StringVar()
        self.status_text.set("")

        self.parent = parent
        self.ip_info = Data_Flow.get_ip_data()
        self.ip_answer_key = self.ip_info[0]
        self.ip_questions = self.ip_info[1]
        self.lesson_id = self.ip_info[2]
        self.labelframeone = ttk.Labelframe(self, width = parent.screen_width/2.0, height = parent.screen_height/2.1, text="Independent Practice", relief=tk.RAISED,style='Red.TLabelframe',borderwidth=0)
        self.labelframetwo = ttk.Labelframe(self, width = parent.screen_width/2.0, height = parent.screen_height/3.1,text="Evaluate", relief=tk.RIDGE,style='Red.TLabelframe')
        self.play_button = ttk.Button(self.labelframetwo, text="Take a Picture", command= lambda: self.play_video(),style='Green.TButton')
        self.qp_button = ttk.Button(self.labelframetwo, text="Print Question Paper", command= lambda: self.gen_question_paper(self.lesson_id),style='Green.TButton')
        #self.qp_answer_button = ttk.Button(self.labelframetwo,text="Easy Answer Sheets", command = lambda: self.gen_ip_sheets(self.lesson_id),style='Green.TButton')
        self.play_button.grid(row=0,column=0,padx=20)
        self.qp_button.grid(row=0,column=1,padx=20)

        #self.qp_answer_button.grid(row=0, column=2, padx=20)
        self.labelframeone.grid_propagate(False)
        self.labelframetwo.grid_propagate(False)
        self.labelframeone.grid(row=0, pady=0, padx = 20,)
        self.labelframetwo.grid(row=1, pady= 10, padx = 20)
        self.notes_text = tk.Text(self.labelframeone,borderwidth=3,highlightthickness=0,
                                     font=("TkCaptionFont", 12,'italic'), foreground="PeachPuff2",background='dark slate gray', wrap=tk.WORD,
                                     width=int(parent.screen_width/22), height = int(parent.screen_height/50))
        self.notes_text.insert(1.0,self.ip_questions)
        self.textscroll = ttk.Scrollbar(self.labelframeone)
        self.notes_text.config(yscrollcommand=self.textscroll.set)
        self.textscroll.config(command=self.notes_text.yview, style='TScrollbar')
        self.status_label = ttk.Label(self.labelframetwo, textvariable=self.status_text, font=("TkCaptionFont", 14), foreground="PeachPuff2",background='dark slate gray')
        self.status_label.grid(row=1, columnspan=3,pady=50)
        self.notes_text.grid(row=0,column=0,sticky=tk.NSEW,padx = 20, pady=30)
        self.textscroll.grid(row=0,column=3,sticky=tk.NSEW)
        #self.status_text.set("To save an image to images folder use \'s\' key.\nSaved in \'classroom_images\' folder")

        parent.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def play_video(self):
        messagebox.showinfo(" Camera Info",
                            "Camera shouldopen in a seperate window. Press the key 's' to save the picture under \n" + imageroot + os.path.sep+"saved_images"+os.path.sep+"classroom_images folder")

        p = Process(target=cv2practice.video_cam_play(imageroot))
        p.start()
        #p.join()  #
        return



    def gen_ip_sheets(self,lessonid):
        pageutils.generate_ip_sheets(lessonid)
        messagebox.showinfo("Answer Sheets Info", "IP Sheets for the class generated in the AnswerSheets folder")

    def gen_question_paper(self,lessonid):

        messagebox.showinfo("Question Paper Info", "Question Paper generated in \n"+imageroot+os.path.sep+"QuestionPapers folder")

        pageutils.generate_ip_paper(lessonid, imageroot)




    def pause_video(self):
        cv2.destroyAllWindows()


    '''def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:

            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels




                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format





                # if the panel is not None, we need to initialize it


        except RuntimeError:
            print("[INFO] caught a RuntimeError")'''

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")

        self.quit()


if __name__== "__main__":
        app = tk.Tk()
        app.geometry("800x800")


        frame = MagicIndenpendentPractice(app,outputPath="../videos")

        frame.grid(row=0)
        app.mainloop()










