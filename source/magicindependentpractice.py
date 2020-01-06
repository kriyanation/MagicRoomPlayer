import os
import tkinter as tk
from tkinter import ttk, StringVar
import Data_Flow
import  sys
from multiprocessing import Process
from PIL import Image
from PIL import ImageTk
import threading
import imutils
import cv2
import time
from imutils.video import VideoStream
import cv2practice
import pageutils


_isLinux = sys.platform.startswith('linux')

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'

class MagicIndenpendentPractice(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)



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
        self.labelframeone = ttk.Labelframe(self, width = parent.screen_width/1.5, height = parent.screen_height/2, text="Independent Practice", relief=tk.RAISED)
        self.labelframetwo = ttk.Labelframe(self, width = parent.screen_width/1.5, height = parent.screen_height/2,text="Evaluate", relief=tk.RIDGE)
        self.play_button = ttk.Button(self.labelframetwo, text="Camera On", command= lambda: self.play_video())
        self.qp_button = ttk.Button(self.labelframetwo, text="Question Paper", command= lambda: self.gen_question_paper(self.lesson_id))
        self.qp_answer_button = ttk.Button(self.labelframetwo,text="Easy Evaluate Sheets", command = lambda: self.gen_ip_sheets(self.lesson_id))
        self.play_button.grid(row=0,column=0,padx=20)
        self.qp_button.grid(row=0,column=1,padx=20)
        self.qp_answer_button.grid(row=0, column=2, padx=20)
        self.labelframeone.grid_propagate(False)
        self.labelframetwo.grid_propagate(False)
        self.labelframeone.grid(row=0, pady=20, padx = 20)
        self.labelframetwo.grid(row=1, pady= 20, padx = 20)
        self.notes_label = ttk.Label(self.labelframeone, text=self.ip_questions,
                                     font=("TkCaptionFont", 16), foreground="dark olive green", wraplength=parent.screen_width/1.8)
        self.status_label = ttk.Label(self.labelframetwo, textvariable=self.status_text, font=("TkCaptionFont", 12), foreground="red")
        self.status_label.grid(row=1, columnspan=3)
        self.notes_label.grid(row=0)


        parent.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def play_video(self):
        p = Process(target=cv2practice.video_cam_play)
        p.start()
        #p.join()  #
        self.status_text.set("Camera opened in another window, to save an image to images folder use 's' key.")
        return



    def gen_ip_sheets(self,lessonid):
        pageutils.generate_ip_sheets(lessonid)
        self.status_text.set("IP Sheets for the class generated in the AnswerSheets folder")

    def gen_question_paper(self,lessonid):
        pageutils.generate_ip_paper(lessonid)
        self.status_text.set("Question Paper generated in the QP folder")




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










