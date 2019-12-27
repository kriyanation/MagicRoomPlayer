import tkinter as tk
from tkinter import ttk
import Data_Flow
class MagicLeaderBoard(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.leaderboard = ttk.LabelFrame(self, text = "Class Leaderboard")
        self.leaderboard.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.headernamelabel = ttk.Label(self.leaderboard, text="Name", font = ('TkDefaultFont', 16), foreground = 'blue')
        self.headerbadgelabel = ttk.Label(self.leaderboard, text="Badge", font=('TkDefaultFont', 16), foreground='blue')
        self.headerpointslabel = ttk.Label(self.leaderboard, text="Points", font=('TkDefaultFont', 16), foreground='blue')

        self.headernamelabel.grid(row=0, column=0, padx=10, pady=2)
        self.headerbadgelabel.grid(row=0, column=1,padx=10, pady=2)
        self.headerpointslabel.grid(row=0, column=2,padx=10, pady=2)

        list_names = Data_Flow.class_info()
        rowindex = 1
        self.badge_image_medal = tk.PhotoImage(file= '../images/medal.png' )
        self.badge_image_normal = tk.PhotoImage(file= '../images/premium-badge.png' )
        for element in list_names:
            self.datanamelabel = ttk.Label(self.leaderboard, text=element[0].strip(), font = ('TkDefaultFont', 12),
                                           foreground = 'green',wraplength = 100)
            if element[1].strip() == 'm':
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medal)
            else:
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_normal)

            self.datapointslabel = ttk.Label(self.leaderboard, text=element[2], font=('TkDefaultFont', 12),
                                           foreground='green')
            self.datanamelabel.grid(row=rowindex, column=0, padx=10, pady=3,sticky=tk.W)
            self.databadgelabel.grid(row=rowindex, column=1, padx=10, pady=3)
            self.datapointslabel.grid(row=rowindex, column=2, padx=10, pady=3)
            rowindex += 1


