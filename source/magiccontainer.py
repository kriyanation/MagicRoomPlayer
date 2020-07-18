import logging

import os
import tkinter as tk
from tkinter import ttk

import Data_Flow_Player

import Timer_Display
import lesson_list_player
import magicapplicationexperiment

import magicfactualpage
import magicindependentpractice
import magicleaderboard
import magictitlepage
import random

import tooltip

logger = logging.getLogger("MagicLogger")

class MagicApplication(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.info("Player container initialized")
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure('Green.TButton', background='white', foreground='royalblue4',font=('helvetica', 12, 'bold'),bordercolor="royalblue4")
        s.map('Green.TButton', background=[('active', '!disabled', 'cyan'), ('pressed', 'white')],
              foreground=[('pressed', 'royalblue4'), ('active', 'royalblue4')])

        s.configure('TScrollbar', background='royalblue4', foreground='deepskyblue4')
        s.map('TScrollbar', background=[('active', '!disabled', 'deepskyblue4'), ('pressed', 'snow')],
              foreground=[('pressed', 'royalblue4'), ('active', 'royalblue4')])
        s.configure('Red.TLabelframe', background='deepskyblue4', bordercolor="royalblue4")
        s.configure('Red.TLabelframe.Label', font=('helvetica', 15, 'bold'))
        s.configure('Red.TLabelframe.Label', foreground='white')
        s.configure('Red.TLabelframe.Label', background='deepskyblue4')

        self.title("Learning Room")
        self.configure(background='deepskyblue4')
        self.headerimage = tk.PhotoImage(file="../images/learning.png")
        ttk.Label(self, text="Learning Room", image=self.headerimage, compound=tk.RIGHT, background='deepskyblue4',
                  font=("helvetica", 18, 'bold'), foreground='white').pack(side=tk.TOP)
        self.tool_frame = tk.Frame(self, background="deepskyblue4")
        self.lbbutton_hide = ttk.Button(self.tool_frame,text="Leader Board", command=self.show_leaderboard_seperate,
                                        style='Green.TButton')
        self.timer_button = ttk.Button(self.tool_frame,text="Timer", command=self.launch_timer,
                                        style='Green.TButton')
        self.timer_button.tooltip = tooltip.ToolTip(self.timer_button, "Launch Timer\nctrl-t")
        self.lbbutton_hide.tooltip = tooltip.ToolTip(self.lbbutton_hide, "Launch Leaderboard\nctrl-l")
        self.tool_frame.pack(side=tk.TOP, anchor=tk.NE, pady=5, padx=5)
        self.lbbutton_hide.pack(side=tk.RIGHT, anchor=tk.NE, pady=5,padx=5)
        self.timer_button.pack(side=tk.RIGHT, anchor=tk.NE, pady=5,padx=5)
        self.show_hide_flag = 1
        app = lesson_list_player.MagicLessonList(parent=self)
        app.geometry("350x600+50+50")
        self.wait_window(app)
        if hasattr(self,"selected_lessons") is False:
            self.destroy()
        print(self.selected_lessons)
        Data_Flow_Player.TEST_ROW=self.selected_lessons[0]
        Data_Flow_Player.imageroot = Data_Flow_Player.file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(Data_Flow_Player.TEST_ROW)+os.path.sep+"images"+os.path.sep
        Data_Flow_Player.videoroot = Data_Flow_Player.file_root + os.path.sep + "Lessons"+os.path.sep+"Lesson" + str(Data_Flow_Player.TEST_ROW)+os.path.sep+ "videos" + os.path.sep
        Data_Flow_Player.saved_canvas = Data_Flow_Player.file_root + os.path.sep +"Lessons"+os.path.sep+"Lesson" + str(Data_Flow_Player.TEST_ROW) +os.path.sep+ "saved_boards"
        self.page_index = 0
        self.resizable(width= True, height= True)
        s = ttk.Style()
        s.theme_use('clam')
        #[('pressed' ,'dark olive green'),('active','white')],foreground=[('pressed','PeachPuff2'),('active', 'PeachPuff2')])
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.bframe = tk.Frame(self,background="deepskyblue4",width=100,height=50)

        self.nextimage = tk.PhotoImage(file="../images/next.png")
        self.nextbutton = ttk.Button(self.bframe,text="Next Step", image=self.nextimage,
                                     command=lambda: self.show_next_page(self.page_index), style='Green.TButton')
        self.backimage = tk.PhotoImage(file="../images/back.png")
        self.backbutton = ttk.Button(self.bframe,text="Last Step", image=self.backimage,
                                     command=lambda: self.show_previous_page(self.page_index), style='Green.TButton')
        self.nextbutton.tooltip = tooltip.ToolTip(self.nextbutton, "Move Next")
        self.backbutton.tooltip = tooltip.ToolTip(self.backbutton, "Move Back")
        self.nextbutton.pack(side = tk.RIGHT, anchor = tk.NE)
        self.backbutton.pack(side=tk.TOP, anchor=tk.NE,padx = 10)
        self.show_title_page()

        self.bind_all('<Control-Key-t>', self.launch_timer)
        self.bind_all('<Control-Key-l>', self.show_leaderboard_seperate)
        self.bind_all('<Right>', lambda event,index=self.page_index:self.show_next_page(self.page_index,event))
        self.bind_all('<Left>', lambda event, index=self.page_index: self.show_previous_page(self.page_index, event))

    def  launch_timer(self,event=None):
        logger.info("TImer launch in player")
        launch_timer = Timer_Display.TimerDisplay(self)
        launch_timer.geometry("240x250+200+200")
        launch_timer.resizable(width=False,height=False)
        launch_timer.attributes("-topmost", True)

    def show_title_page(self):
        logger.info("Player show_title_page")
        self.backbutton.configure(state="disabled")
        if self.page_index == 1:
            self.factual_page.forget()
            self.bframe.pack_forget()

        self.TitlePage = magictitlepage.MagicTitlePage(self)
        self.TitlePage.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH, expand=True)
        self.bframe.pack(side=tk.BOTTOM, anchor=tk.NE, padx=5, pady=20)



    def show_next_page(self, index,event=None):
        logger.info("Player show_next_page")
        ap_mode = Data_Flow_Player.get_application_mode()
        if index == 0:
            self.show_factual_page(ap_mode)
            self.page_index += 1
            return
        if index == 1:
            if ap_mode == "Video":
                self.show_video_page()
                self.page_index += 1
            else:
                self.show_experiment_page()

                self.page_index += 1
            return
        if index == 2:
            self.show_ip_page(ap_mode)
            self.page_index += 1

    def show_previous_page(self, index,event=None):
        logger.info("Player show_previous_page")
        ap_mode = Data_Flow_Player.get_application_mode()
        if index == 1:
            self.show_title_page()
            self.page_index -= 1
            return
        if index == 2:
            self.show_factual_page(ap_mode)
            self.page_index -= 1
            return
        if index == 3:

            self.show_experiment_page()

            self.page_index -= 1
            return


    def show_ip_page(self, ap_mode):
        logger.info("Player show_ip_page")
        self.nextbutton.configure(state="disabled")
        self.show_hide_flag = 1
        #self.application_experiment_page.save_image_window(self.application_experiment_page.canvas_experiment, random.randint(0,100))

        self.bframe.pack_forget()

        self.application_experiment_page.forget()
        self.independent_practice = magicindependentpractice.MagicIndenpendentPractice(self)

        self.independent_practice.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, anchor=tk.N)
        self.bframe.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5,pady=30)

    def show_experiment_page(self):
        logger.info("Player show_experiment_page")
        self.nextbutton.configure(state="active")
        if self.page_index == 3:
            self.independent_practice.pack_forget()
        else:
            self.factual_page.pack_forget()

        self.bframe.pack_forget()
        self.application_experiment_page = magicapplicationexperiment.MagicExperimentPage(self)
        self.bframe.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5, pady=30)
        self.application_experiment_page.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, anchor=tk.N)


    def show_leaderboard_seperate(self,event=None):
        logger.info("Player show_leaderboard_seperate")
        win = tk.Toplevel()
        win.wm_title("Leaderboard")
        win.wm_geometry('340x500+100+100')
        win.configure(background='deepskyblue4')
        win.resizable(width=False, height=False)
        win.attributes("-topmost", True)
        self.leaderboard = magicleaderboard.MagicLeaderBoard(win,mode="top")
        self.leaderboard.grid(row=0, column=0)

        b = ttk.Button(win, text="Close", style='Green.TButton', command=win.destroy)
        b.grid(row=1, column=0,pady=5)

    def show_factual_page(self,ap_mode):
        logger.info("Player show_factual_page")
        self.backbutton.configure(state="active")
        if self.page_index == 2:
            self.application_experiment_page.forget()
        else:
            self.TitlePage.pack_forget()

        self.bframe.pack_forget()
        self.factual_page = magicfactualpage.MagicFactualPage(self)
        self.factual_page.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, anchor=tk.N)

        self.bframe.pack(side=tk.BOTTOM, anchor=tk.SE, padx=5,pady=30)




    def  Configure(self,event):
        self.screen_width = self.winfo_width()
        self.screen_height = self.winfo_height()
       # self.application_experiment_page.canvas_experiment.configure(width=self.winfo_width() / 1.5,
       #                                      height=self.winfo_height() / 2)

       # print(str(self.screen_width) + ',' + str(self.screen_height))










# if __name__ == "__main__":
#
#     multiprocessing.freeze_support()
#     app = MagicApplication()
#     screen_width = app.winfo_screenwidth()
#     screen_height = app.winfo_screenheight()
#
#
#     app.geometry(str(screen_width)+'x'+str(screen_height)+'+5+5')
#
#
#
#     #app.bind("<KeyPress-Down>", app.show_title_text)
#     app.bind('<Configure>',app.Configure)
#     app.mainloop()

