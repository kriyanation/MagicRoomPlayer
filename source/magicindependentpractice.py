import tkinter as tk
from tkinter import ttk
import Data_Flow
import  sys
from PIL import Image
from PIL import ImageTk
import threading
import imutils
import cv2
import time
from imutils.video import VideoStream


_isLinux = sys.platform.startswith('linux')

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'

class MagicIndenpendentPractice(tk.Frame):
    def __init__(self, parent, outputPath, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.panel = None

        self.parent = parent
        self.ip_info = Data_Flow.get_ip_data()
        self.ip_answer_key = self.ip_info[0]
        self.ip_questions = self.ip_info[1]
        self.labelframeone = ttk.Labelframe(self, width = 1200, height = 400, text="Independent Practice", relief=tk.RAISED)
        self.labelframetwo = ttk.Labelframe(self, width = 1200, height = 500,text="Evaluate", relief=tk.RIDGE)
        self.play_button = ttk.Button(self.labelframetwo, text="Camera On", command= self.play_video)
        self.off_button = ttk.Button(self.labelframetwo, text="Camera off", command= self.pause_video)
        self.play_button.grid(row=0,column=0,padx=20)
        self.off_button.grid(row=0,column=1,padx=20)
        self.labelframeone.grid_propagate(False)
        self.labelframetwo.grid_propagate(False)
        self.labelframeone.grid(row=0, pady=20, padx = 20)
        self.labelframetwo.grid(row=1, pady= 20, padx = 20)
        self.notes_label = ttk.Label(self.labelframeone, text=self.ip_questions,
                                     font=("TkCaptionFont", 16), foreground="dark olive green", wraplength=900)
       # self.notes_label.grid(row=0)


        parent.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def play_video(self):
        self.vs= VideoStream().start()
        self.stopEvent = threading.Event()

        self.thread = threading.Thread(target=self.videoLoop, args=())

        self.thread.start()


    def pause_video(self):
        self.panel.grid_forget()
        self.vs.stop()
        self.stopEvent.set()
        self.panel = None


    def videoLoop(self):
        # DISCLAIMER:
        # I'm not a GUI developer, nor do I even pretend to be. This
        # try/except statement is a pretty ugly hack to get around
        # a RunTime error that Tkinter throws due to threading
        try:

            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels


                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=600, height=300)


                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

                image = Image.fromarray(image)

                image = ImageTk.PhotoImage(image)




                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = tk.Label(self.labelframetwo,image=image)
                    self.panel.image = image
                    self.panel.grid(row=1,column=0,columnspan=2, padx=80, pady=10)

                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.quit()


if __name__== "__main__":
        app = tk.Tk()
        app.geometry("800x800")

      #  vs = VideoStream().start()
        frame = MagicIndenpendentPractice(app,outputPath="../videos")
        time.sleep(2.0)
        frame.grid(row=0)
        app.mainloop()










