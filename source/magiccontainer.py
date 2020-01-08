import tkinter as tk
from tkinter import ttk
import magicleaderboard, magictitlepage, magicapplicationexperiment,magicapplicationvideo,magicindependentpractice
import scroll_bars
import Data_Flow

import magicfactualpage



class MagicApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.title("Magic Room")
        #self.backgroundimage = tk.PhotoImage(file="../images/sky.png")
        #self.backgroundlabel = tk.Label(self, image=self.backgroundimage)
        #self.backgroundlabel.place(x=0,y=0,relwidth=1,relheight=1)
        self.configure(background='dark slate gray')


        self.page_index = 0
        self.resizable(width= True, height= True)
        s = ttk.Style()
        s.configure('Green.TButton', background='dark slate gray',foreground='PeachPuff2')
        s.map('Green.TButton',background=[('active','!disabled','dark olive green'),('pressed','PeachPuff2')], foreground=[('pressed','PeachPuff2'),('active','PeachPuff2')])
        #[('pressed' ,'dark olive green'),('active','white')],foreground=[('pressed','PeachPuff2'),('active', 'PeachPuff2')])
        ttk.Label(self, text="SGV Magic Player",background='dark slate gray', font=("courier", 22,'bold','italic'),foreground = 'PeachPuff2').pack(side = tk.TOP)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        self.TitlePage = magictitlepage.MagicTitlePage(self)
        #self.factual_page = magicfactualpage.MagicFactualPage(self)
        #self.application_experiment_page = magicapplicationexperiment.MagicExperimentPage(self)
        #self.application_video_page = magicapplicationvideo.MagicApplicationVideo(self)
        #self.independent_practice = magicindependentpractice.MagicIndenpendentPractice(self)
        self.keydown = 0
        print(str(self.screen_width) + ',' + str(self.screen_height))
        self.pack_propagate(False)
        self.TitlePage.pack(side = tk.LEFT, anchor= tk.N)
        self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self)
        self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE)
        #self.TitlePage.pack(side=tk.LEFT, fill=tk.BOTH)
        self.nextbutton = ttk.Button(text = "Next Step", command = lambda: self.show_next_page(self.page_index),style='Green.TButton')
        self.nextbutton.pack(side = tk.BOTTOM, anchor = tk.SE)




    def show_next_page(self, index):
        ap_mode = Data_Flow.get_application_mode()
        if index == 0:
            self.TitlePage.player.stop()
            self.TitlePage.pack_forget()
            self.LeaderBoard.pack_forget()
            self.factual_page = magicfactualpage.MagicFactualPage(self)
            self.factual_page.pack(side = tk.LEFT)
            self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self)
            self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE)
            self.page_index += 1
            return
        if index == 1:
            self.factual_page.pack_forget()
            self.LeaderBoard.pack_forget()
            self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self)
            self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE)

            if ap_mode == "Video":
                self.application_video_page = magicapplicationvideo.MagicApplicationVideo(self)
                self.application_video_page.pack(side=tk.LEFT)

                self.page_index += 1

            else:
                self.application_experiment_page = magicapplicationexperiment.MagicExperimentPage(self)
                self.application_experiment_page.pack(side=tk.LEFT)

                self.page_index += 1
            return

        if index == 2:
            self.LeaderBoard.pack_forget()
            self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self)
            self.LeaderBoard.pack(side=tk.RIGHT, anchor=tk.NE)
            if ap_mode == "Video":

                self.application_video_page.pack_forget()
                self.independent_practice = magicindependentpractice.MagicIndenpendentPractice(self)
                self.independent_practice.pack(side=tk.LEFT)

            else:
                self.application_experiment_page.pack_forget()
                self.independent_practice = magicindependentpractice.MagicIndenpendentPractice(self)
                self.independent_practice.pack(side=tk.LEFT)
            self.page_index += 1



    def  Configure(self,event):
        self.screen_width = self.winfo_width()
        self.screen_height = self.winfo_height()
        print(str(self.screen_width) + ',' + str(self.screen_height))

    def show_leader_board(self,event):
        #print("R Pressed")

        self.LeaderBoard.pack(side=tk.RIGHT, fill=tk.BOTH)
    def hide_leader_board(self, event):
        #print("o pressed")
        self.LeaderBoard.pack_forget()

    def show_title_text(self, event):
        print("Down pressed")
        if (self.keydown == 0):
            self.TitlePage.title_intro()
            self.keydown += 1
            return
        if (self.keydown == 1):
            self.TitlePage.title_video()
            self.keydown += 1






if __name__ == "__main__":


    app = MagicApplication()
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()


    app.geometry(str(screen_width)+'x'+str(screen_height)+'+5+5')
    app.bind("<KeyPress-r>", app.show_leader_board)
    app.bind("<KeyPress-o>", app.hide_leader_board)
    app.bind("<KeyPress-Down>", app.show_title_text)
    app.bind('<Configure>',app.Configure)

    app.mainloop()
