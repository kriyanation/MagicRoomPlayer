import tkinter as tk
from multiprocessing import Process
from tkinter import ttk, StringVar

import cv2
import pyzbar.pyzbar as pyzbar


class MagicAnswerSheetScanner(tk.Tk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.labelframe_scanner_output = ttk.Labelframe(self, text="Scanner Output",width=600, height=500)
        self.codeoutput = StringVar()
        self.textoutput =tk.Text(self.labelframe_scanner_output,height =20,width=200)
        self.textoutput.insert(1.0,self.codeoutput.get())
        self.labelframe_scanner_output.grid(row = 0)
        self.textoutput.grid(row = 0)
        self.start_scanning_button = ttk.Button(self.labelframe_scanner_output,text='Start Scanning',command=self.start_scanner_app)
        self.start_scanning_button.grid(row=1,column=0)

    def start_scanner_app(self):
        p = Process(target=self.video_cam_play)
        p.start()
    def video_cam_play(self):
        cap = cv2.VideoCapture(2)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        found = False
        while True:
            ret, frame = cap.read()
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
            cv2.imshow('Input', frame)
            decodedObjects = self.decode(frame)
            # frame, found = display(frame, decodedObjects)
            cv2.imshow('Input', frame)
            if found == True:
                cv2.waitKey(0)
                print("Should I save the image?")
            c = cv2.waitKey(1)
            if cv2.getWindowProperty('Input', cv2.WND_PROP_VISIBLE) < 1:
                break
            # if c == 27:
            #   break

        cap.release()
        cv2.destroyAllWindows()

    def decode(self, image):
       # print('decoding')

        decodedobjects = pyzbar.decode(image)
        for obj in decodedobjects:
            print('type: ', obj.type)
            print("data: ", obj.data, "\n")
            file_interpreter = open('raw_interpreter.txt','w+')
            file_interpreter.write(str(obj.data)+'\n')

        return decodedobjects


if __name__ == '__main__':
    app = MagicAnswerSheetScanner()



    # Check if the webcam is opened correctly

    app.mainloop()