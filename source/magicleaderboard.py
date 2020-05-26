import tkinter as tk
from tkinter import ttk, StringVar

import Data_Flow_Player
import tooltip


class MagicLeaderBoard(tk.Frame):
    def __init__(self, parent,mode="inline", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent=parent
        self.mode = mode
        self.configure(background='steelblue3',borderwidth=0)
        s = ttk.Style(self)
        s.configure('Red.TLabelframe', background='steelblue3')
        s.configure('Red.TLabelframe.Label', font=('helvetica', 12, 'bold'))
        s.configure('Red.TLabelframe.Label', foreground='white')
        s.configure('Red.TLabelframe.Label', background='steelblue3')



       # self.leaderboard = ttk.LabelFrame(self, text = "Class Leaderboard", width=parent.screen_width/4, height=parent.screen_height,borderwidth=8,relief=tk.GROOVE,style='Red.TLabelframe')
        self.c_canvas = tk.Canvas(self, background='white',borderwidth=0,highlightthickness=0)

        self.c_canvas.grid(row=0, column=0)
        self.leaderboard = tk.Frame(self.c_canvas,
                                           borderwidth=0,
                                          background='white')
        self.dataframe= tk.Frame(self.leaderboard)
        self.dataframe.configure(background='white')
        self.saveimage = tk.PhotoImage(file="../images/floppy.png")
       # self.refreshbutton = ttk.Button(self.dataframe,text="Refresh",style='Green.TButton',command=self.refresh_data,cursor="arrow")
        self.savebutton = ttk.Button(self.dataframe,text="Save",image = self.saveimage, style='Green.TButton',command=self.save_data,cursor="arrow")
        self.savebutton.tooltip = tooltip.ToolTip(self.savebutton, "Save Changes")
        self.dataframe.grid(row=0,column=3,sticky=tk.E)
        #self.refreshbutton.grid(row=0,column=0)
        self.savebutton.grid(row=0,column=3,padx=5,sticky=tk.W)

        self.scrollbar = ttk.Scrollbar(self)
        self.c_canvas.config(yscrollcommand=self.scrollbar.set)
        self.c_canvas.create_window((0, 0), window=self.leaderboard,anchor='nw')
        self.leaderboard.bind("<Configure>", self.c_function)
        self.scrollbar.grid(row=0,column=3,sticky="nsew")

        self.scrollbar.config(command=self.c_canvas.yview, style='TScrollbar')
        #self.leaderboard.grid(row=0, column=0, sticky=tk.W + tk.E)
        self.headernamelabel = ttk.Label(self.leaderboard, text="Name", font = ('TkDefaultFont', 16,'bold'),background='white', foreground = 'midnight blue')
        self.headerbadgelabel = ttk.Label(self.leaderboard, text="Badge", font=('TkDefaultFont', 16,'bold'),background='white', foreground='midnight blue')
        self.headerpointslabel = ttk.Label(self.leaderboard, text="Points",font=('TkDefaultFont', 16,'bold'),background='white', foreground='midnight blue')

        self.headernamelabel.grid(row=0, column=0, padx=0, pady=2)
        self.headerbadgelabel.grid(row=0, column=1,padx=10, pady=2)
        self.headerpointslabel.grid(row=0, column=2, pady=2)
        self.refresh_data()

    def c_function(self, event):
        if self.mode == "inline":
            self.c_canvas.configure(scrollregion=self.c_canvas.bbox("all"),borderwidth=0,width=self.parent.winfo_width()/4,height=self.parent.winfo_height()-300)
        else:
            self.c_canvas.configure(scrollregion=self.c_canvas.bbox("all"), borderwidth=0,width=320,
                                    height=300)
    def refresh_data(self):

        self.spinboxvalue = []
        self.list_points = []

        list_names = Data_Flow_Player.class_info()
        rowindex = 2
        self.badge_image_medala = tk.PhotoImage(file= '../images/medala.png' )
        self.badge_image_medalb = tk.PhotoImage(file= '../images/medalb.png' )
        self.badge_image_medalc = tk.PhotoImage(file='../images/medalc.png')
        for element in list_names:
            self.datanamelabel = ttk.Label(self.leaderboard, text=element[0].strip(), font = ('TkDefaultFont', 12,'bold'),
                                           foreground = 'midnight blue',wraplength = 80,background='white')
            if element[1].strip() == 'a':
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medala,background='white')
            elif element[1].strip() == 'b':
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medalb,background='white')
            else:
                self.databadgelabel = ttk.Label(self.leaderboard, image=self.badge_image_medalc,
                                                background='white')

            points = StringVar()
            points.set(str(element[2]))
            self.spinboxvalue.append(points)
            print("rowindex"+str(rowindex))
            self.datapointspinner = ttk.Spinbox(self.leaderboard,background='white',foreground='midnight blue',font=('helvetica', 12,"bold"),
                                                from_=0,to=100,textvariable=self.spinboxvalue[rowindex-2],wrap=True,width=2)

            self.list_points.append((element[0],self.spinboxvalue[rowindex-2]))

           # self.datapointslabel = ttk.Label(self.leaderboard, text=element[2], font=('TkDefaultFont', 12),
           #                                foreground='PeachPuff2',background='dark slate gray')
            self.datanamelabel.grid(row=rowindex, column=0, padx=10, pady=3,sticky=tk.W)
            self.databadgelabel.grid(row=rowindex, column=1, padx=10, pady=3)
            self.datapointspinner.grid(row=rowindex, column=2, pady=3)
            rowindex += 1


    def save_data(self):
        Data_Flow_Player.save_leader_board_data(self.list_points)
        self.refresh_data()




