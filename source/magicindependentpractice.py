import logging
import tkinter as tk
from tkinter import ttk, StringVar
import tkinter as tk
from tkinter import ttk, StringVar,scrolledtext
import sys


import Data_Flow_Player

_isLinux = sys.platform.startswith('linux')

DEFAULT_PEN_SIZE = 5.0
DEFAULT_COLOR = 'black'

logger = logging.getLogger("MagicLogger")

class MagicIndenpendentPractice(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        logger.info("Independent Practice Initialize")
        self.configure(background='deepskyblue4')
        self.unbind_all('<Control-Key-n>')


        self.bind("<Configure>",self.resize_t)
        self.cameraoff = False
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.panel = None
        self.status_text = StringVar()
        self.status_text.set("")

        self.parent = parent
        self.ip_info = Data_Flow_Player.get_ip_data()
        self.ip_answer_key = self.ip_info[0]
        self.ip_questions = self.ip_info[1]
        self.lesson_id = self.ip_info[2]
        self.labelframeone = ttk.Labelframe(self, text="Learning Assessment/Notes", relief=tk.RAISED,style='Red.TLabelframe',borderwidth=0)

        self.labelframeone.grid(row=0, pady=0, padx = 20,sticky = tk.NSEW)


        self.notes_text = tk.Text(self.labelframeone,borderwidth=3,highlightthickness=0,
                                     font=("helvetica", 14
                                           ,'bold'), foreground="royalblue4",background='white', wrap=tk.WORD)

        self.notes_text.insert(1.0,self.ip_questions)
        self.textscroll = ttk.Scrollbar(self.labelframeone)
        self.notes_text.config(yscrollcommand=self.textscroll.set)
        self.textscroll.config(command=self.notes_text.yview, style='TScrollbar')

        self.notes_text.grid(row=0,column=0,sticky=tk.NSEW,padx = 20, pady=10)
        self.textscroll.grid(row=0,column=3,sticky=tk.NSEW)
        #self.status_text.set("To save an image to images folder use \'s\' key.\nSaved in \'classroom_images\' folder")
        self.answer_button = ttk.Button(self.labelframeone, text="Answer",
                                         width=8,
                                         command=self.answer_questions, style='Green.TButton')
        self.answer_button.grid(row=1,column=0,columnspan=2)

    def resize_t(self,event):
        self.notes_text.configure(width=int(self.winfo_width()/25),height=int(self.winfo_height()/45))

    def answer_questions(self):
        self.answer_screen = tk.Toplevel(self)
        self.answer_screen.title("Enter Answers")
        self.answer_screen.geometry("650x550+300+200")
        self.answer_screen.configure(background="deepskyblue4")
        answer_submitted = Data_Flow_Player.get_answer()
        self.answer_label = ttk.Label(self.answer_screen, text="Enter your answers here",
                                      background='deepskyblue4', foreground='white',
                                      font=("helvetica", 16, 'bold'))

        self.scroll_t = scrolledtext.ScrolledText(self.answer_screen,wrap=tk.WORD,width=50,height=20,font=("Helvetica",12))
        self.scroll_t.vbar.configure(background="deepskyblue4")
        self.answer_label.grid(row=0,column=0,padx=30,pady=10)
        self.scroll_t.grid(row=1, column=0, padx=30, pady=10)
        if answer_submitted is not None:
            self.scroll_t.insert("1.0",answer_submitted)

        self.submit_button = ttk.Button(self.answer_screen, text="Save Answer",
                                        width=16,
                                        command=self.save_answers, style='Green.TButton')
        self.submit_button.grid(row=2, column=0, columnspan=2)

    def save_answers(self):
        answer_text = self.scroll_t.get("1.0", tk.END)
        print(answer_text)
        Data_Flow_Player.set_answer(answer_text)
        self.answer_screen.destroy()


# if __name__== "__main__":
#         app = tk.Tk()
#         app.geometry("800x800")


        # frame = MagicIndenpendentPractice(app,outputPath="../videos")
        #
        # frame.grid(row=0)
        # app.mainloop()










