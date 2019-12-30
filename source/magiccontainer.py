import tkinter as tk
from tkinter import ttk
import magicleaderboard, magictitlepage
import scroll_bars
import ttkthemes
from ttkthemes import ThemedTk
import magicfactualpage



class MagicApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Magic Room")
        self.factual_page = magicfactualpage.MagicFactualPage(self)

        self.resizable(width= True, height= True)


        ttk.Label(self, text="SGV Magic Player", font=("TkDefaultFont", 18),
                  foreground = 'green').pack()
        self.LeaderBoard = magicleaderboard.MagicLeaderBoard(self)

        self.TitlePage = magictitlepage.MagicTitlePage(self)
        self.keydown = 0


        self.TitlePage.pack(side = tk.LEFT)


        self.LeaderBoard.pack(side = tk.RIGHT, fill=tk.BOTH)
        #self.TitlePage.pack(side=tk.LEFT, fill=tk.BOTH)
        self.nextbutton = ttk.Button(text = "Next Step", command = self.show_factual_page)
        self.nextbutton.pack(side = tk.BOTTOM, anchor = tk.SE)

    def show_factual_page(self):
        self.TitlePage.player.stop()
        self.TitlePage.pack_forget()
        self.factual_page.pack(side = tk.LEFT)


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





if __name__ == "__main__":


    app = MagicApplication()

    app.geometry("1280x800+200+200")
    app.bind("<KeyPress-r>", app.show_leader_board)
    app.bind("<KeyPress-o>", app.hide_leader_board)
    app.bind("<KeyPress-Down>", app.show_title_text)

    app.mainloop()
