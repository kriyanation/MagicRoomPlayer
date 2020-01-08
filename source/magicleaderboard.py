import tkinter as tk
from tkinter import ttk
import Data_Flow
class MagicLeaderBoard(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(background='dark slate gray')
        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background='dark slate gray')
        s.configure('Red.TLabelframe.Label', font=('courier', 12, 'bold','italic'))
        s.configure('Red.TLabelframe.Label', foreground='PeachPuff2')
        s.configure('Red.TLabelframe.Label', background='dark slate gray')

        self.leaderboard = ttk.LabelFrame(self, text = "Class Leaderboard", width=parent.screen_width/4, height=parent.screen_height,borderwidth=8,relief=tk.GROOVE,style='Red.TLabelframe')

        self.leaderboard.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.headernamelabel = ttk.Label(self.leaderboard, text="Name", font = ('TkDefaultFont', 16),background='dark slate gray', foreground = 'PeachPuff2')
        self.headerbadgelabel = ttk.Label(self.leaderboard, text="Badge", font=('TkDefaultFont', 16),background='dark slate gray', foreground='PeachPuff2')
        self.headerpointslabel = ttk.Label(self.leaderboard, text="Points", font=('TkDefaultFont', 16),background='dark slate gray', foreground='PeachPuff2')

        self.headernamelabel.grid(row=0, column=0, padx=10, pady=2)
        self.headerbadgelabel.grid(row=0, column=1,padx=10, pady=2)
        self.headerpointslabel.grid(row=0, column=2,padx=10, pady=2)

        list_names = Data_Flow.class_info()
        rowindex = 1
        self.badge_image_medal = tk.PhotoImage(file= '../images/medal.png' )
        self.badge_image_normal = tk.PhotoImage(file= '../images/premium-badge.png' )
        for element in list_names:
            self.datanamelabel = ttk.Label(self.leaderboard, text=element[0].strip(), font = ('TkDefaultFont', 12),
                                           foreground = 'PeachPuff2',wraplength = 100,background='dark slate gray')
            if element[1].strip() == 'm':
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medal,background='dark slate gray')
            else:
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_normal,background='dark slate gray')

            self.datapointslabel = ttk.Label(self.leaderboard, text=element[2], font=('TkDefaultFont', 12),
                                           foreground='PeachPuff2',background='dark slate gray')
            self.datanamelabel.grid(row=rowindex, column=0, padx=10, pady=3,sticky=tk.W)
            self.databadgelabel.grid(row=rowindex, column=1, padx=10, pady=3)
            self.datapointslabel.grid(row=rowindex, column=2, padx=10, pady=3)
            rowindex += 1


