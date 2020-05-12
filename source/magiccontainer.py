import multiprocessing
import os
import tkinter as tk
from tkinter import ttk

import Data_Flow_Player
import LessonList
import Timer_Display
import magicapplicationexperiment
import magicapplicationvideo
import magicfactualpage
import magicindependentpractice
import magicleaderboard
import magictitlepage
import random

import tooltip


class MagicApplication(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure('Green.TButton', background='dark slate gray', foreground='PeachPuff2')
        s.map('Green.TButton', background=[('active', '!disabled', 'dark olive green'), ('pressed', 'PeachPuff2')],
              foreground=[('pressed', 'PeachPuff2'), ('active', 'PeachPuff2')])

        s.configure('TScrollbar', background='dark slate gray', foreground='dark slate gray')
        s.map('TScrollbar', background=[('active', '!disabled', 'dark olive green'), ('disabled', 'dark slate gray')],
              foreground=[('active', 'PeachPuff2'), ('disabled', 'dark slate gray')])

        self.title("Learning Room")
        self.configure(background='dark slate gray')
        self.headerimage = tk.PhotoImage(file="../images/learning.png")
        ttk.Label(self, text="Learning Room", image=self.headerimage, compound=tk.RIGHT, background='dark slate gray',
                  font=("courier", 18, 'bold'), foreground='PeachPuff2').pack(side=tk.TOP)

        self.tool_frame = tk.Frame(self, background="dark slate gray")
        self.lbbutton_hide = ttk.Button(self.tool_frame,text="Show/Hide LeaderBoard", command=self.show_hide_leader_board,
                                        style='Green.TButton')
        self.timer_button = ttk.Button(self.tool_frame,text="Timer", command=self.launch_timer,
                                        style='Green.TButton')
        self.timer_button.tooltip = tooltip.ToolTip(self.timer_button, "Launch Timer App")

        self.tool_frame.pack(side=tk.TOP, anchor=tk.NE, pady=5, padx=5)
        self.lbbutton_hide.pack(side=tk.RIGHT, anchor=tk.NE, pady=5,padx=5)
        self.timer_button.pack(side=tk.RIGHT, anchor=tk.NE, pady=5,padx=5)
        self.show_hide_flag = 1
      #  self.lbbutton_show = ttk.Button(text="Show LeaderBoard", command=self.show_leader_board,
      #                                  style='Green.TButton')

        app = LessonList.MagicLessonList(bg='dark slate gray', fg='white', buttonbg='dark olive green', selectmode=tk.SINGLE,
                              buttonfg='snow',parent=self)
        self.wait_window(app)
        print(self.selected_lessons)
        Data_Flow_Player.TEST_ROW=self.selected_lessons[0]
        Data_Flow_Player.imageroot = Data_Flow_Player.file_root+os.path.sep+"Lessons"+os.path.sep+"Lesson"+str(Data_Flow_Player.TEST_ROW)+os.path.sep+"images"+os.path.sep
        Data_Flow_Player.videoroot = Data_Flow_Player.file_root + os.path.sep + "Lessons"+os.path.sep+"Lesson" + str(Data_Flow_Player.TEST_ROW)+os.path.sep+ "videos" + os.path.sep
        Data_Flow_Player.saved_canvas = Data_Flow_Player.file_root + os.path.sep +"Lessons"+os.path.sep+"Lesson" + str(Data_Flow_Player.TEST_ROW) +os.path.sep+ "saved_boards"

        self.page_index = 0
        self.resizable(width= True, height= True)
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('Green.TButton', background='dark slate gray',foreground='PeachPuff2')
        s.map('Green.TButton',background=[('active','!disabled','dark olive green'),('pressed','PeachPuff2')], foreground=[('pressed','PeachPuff2'),('active','PeachPuff2')])
        #[('pressed' ,'dark olive green'),('active','white')],foreground=[('pressed','PeachPuff2'),('active', 'PeachPuff2')])
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()


        self.show_title_page()

        self.bframe = tk.Frame(self,background="dark slate gray")

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


        self.bframe.pack(side=tk.BOTTOM, anchor=tk.NE, pady=30)
        self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE, pady=5)



    def  launch_timer(self):
        launch_timer = Timer_Display.TimerDisplay(self)
        launch_timer.geometry("240x250+200+200")
        launch_timer.resizable(width=False,height=False)
        launch_timer.attributes("-topmost", True)

    def show_title_page(self):
        if self.page_index == 1:
            self.factual_page.forget()
            self.LeaderBoard.pack_forget()
            self.bframe.pack_forget()

        self.TitlePage = magictitlepage.MagicTitlePage(self)
        self.keydown = 0
        print(str(self.screen_width) + ',' + str(self.screen_height))
       # self.pack_propagate(False)
        self.TitlePage.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH, expand=True)
        self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self,borderwidth=0)
        if self.page_index == 1:
            self.bframe.pack(side=tk.BOTTOM, anchor=tk.SE, pady=30)
            if self.show_hide_flag == 1:
                self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE)



    def show_hide_leader_board(self):
        if self.show_hide_flag == 1:
            self.LeaderBoard.pack_forget()
            self.show_hide_flag=0
        else:
            if (self.page_index != 2):
                self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE, pady=5)
                self.show_hide_flag = 1
            else:
                self.show_leaderboard_seperate()






    def show_next_page(self, index):
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

    def show_previous_page(self, index):
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
            if ap_mode == "Video":
                self.show_video_page()

            else:
                self.show_experiment_page()

            self.page_index -= 1
            return


    def show_ip_page(self, ap_mode):
        self.show_hide_flag = 1
        self.application_experiment_page.save_image_window(self.application_experiment_page.canvas_experiment, random.randint(0,100))
        self.LeaderBoard.pack_forget()
        self.bframe.pack_forget()
        if ap_mode == "Video":
            #self.application_video_page.player.stop()
            self.application_video_page.pack_forget()
        else:
            self.application_experiment_page.forget()
        self.independent_practice = magicindependentpractice.MagicIndenpendentPractice(self)

        self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self)
        self.bframe.pack(side=tk.BOTTOM, anchor=tk.SE, pady=30)
        if self.show_hide_flag == 1:
            self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE)
        self.independent_practice.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, anchor=tk.N)


    def show_video_page(self):
        if self.page_index == 3:
            self.independent_practice.pack_forget()
        else:
            self.factual_page.pack_forget()
        self.LeaderBoard.pack_forget()
        self.bframe.pack_forget()
        self.application_video_page = magicapplicationvideo.MagicApplicationVideo(self)
        self.application_video_page.pack(side=tk.LEFT, anchor=tk.N)
        self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self)
        self.bframe.pack(side=tk.BOTTOM, anchor=tk.SE, pady=30)
        self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE)


    def show_experiment_page(self):
        if self.page_index == 3:
            self.independent_practice.pack_forget()
        else:
            self.factual_page.pack_forget()
        self.LeaderBoard.pack_forget()
        self.bframe.pack_forget()
        self.application_experiment_page = magicapplicationexperiment.MagicExperimentPage(self)



        self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self)
        self.bframe.pack(side=tk.BOTTOM, anchor=tk.SE, pady=30)
        if self.show_hide_flag == 1:
          #self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE)
          pass
        self.show_hide_flag = 0
        self.application_experiment_page.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE, anchor=tk.N)


    def show_leaderboard_seperate(self):
        win = tk.Toplevel()
        win.wm_title("Leaderboard")
        win.wm_geometry('340x400+500+500')
        win.configure(background='dark slate gray')
        self.leaderboard = magicleaderboard.MagicLeaderBoard(win,mode="top")
        self.leaderboard.grid(row=0, column=0)

        b = ttk.Button(win, text="Close", style='Blue.TButton', command=win.destroy)
        b.grid(row=1, column=0)

    def show_factual_page(self,ap_mode):
        if self.page_index == 2:
            if ap_mode == "Video":
                #self.application_video_page.player.stop()
                self.application_video_page.pack_forget()
            else:
                self.application_experiment_page.forget()
        else:
            if hasattr(self.TitlePage,"player"):
                 #self.TitlePage.player.stop()
                  pass
            self.TitlePage.pack_forget()
        self.LeaderBoard.pack_forget()
        self.bframe.pack_forget()
        self.factual_page = magicfactualpage.MagicFactualPage(self)
        self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self)
        self.bframe.pack(side=tk.BOTTOM, anchor=tk.SE, pady=30)
        if self.show_hide_flag == 1:
            self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE)

        self.factual_page.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE,anchor=tk.N)



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

