import configparser
import logging
import os
import random
import sqlite3
import sys
from pathlib import Path
from tkinter import StringVar, messagebox

TEST_ROW = 5

config = configparser.RawConfigParser()
two_up = Path(__file__).parents[2]
imageroot = ""
videoroot = ""
logger = logging.getLogger("MagicLogger")


file_root = os.path.abspath(os.path.join(os.getcwd(),".."))
db = file_root+os.path.sep+"MagicRoom.db"

saved_canvas = ""

def get_Title():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Lesson_Title from Magic_Science_Lessons where Lesson_ID = ?"
    cur.execute(sql, (TEST_ROW, ))
    text = cur.fetchone()[0]
    #print(text)
    connection.commit()
    connection.close()
    return text
 except sqlite3.OperationalError:
     messagebox.showwarning("Title text could not be retrieved")
     logger.exception("Title text could not be retrieved")


def get_Lessons():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Lesson_ID, Lesson_Title from Magic_Science_Lessons"
    cur.execute(sql)
    rows = cur.fetchall()
    list_lessons = []
    for element in rows:
        list_lessons.append(element)
    connection.commit()
    connection.close()
    return list_lessons
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")

def get_link():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Apply_External_Link from Magic_Science_Lessons where Lesson_ID=?"
    cur.execute(sql,(TEST_ROW,))
    external_link = cur.fetchone()[0]
    print(external_link)


    connection.commit()
    connection.close()
    return external_link
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")

#get_Title()

def get_title_image():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Title_Image from Magic_Science_Lessons where Lesson_ID = ?"
    cur.execute(sql, (TEST_ROW, ))
    text = cur.fetchone()[0]
    print(text)
    connection.commit()
    connection.close()
    return imageroot+text
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")

def get_title_video():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Title_Video from Magic_Science_Lessons where Lesson_ID = ?"
    cur.execute(sql, (TEST_ROW, ))
    text = cur.fetchone()[0]
    #print(text)
    connection.commit()
    connection.close()
    if("/" in text):
        return text
    return videoroot+text
 except sqlite3.OperationalError:
    messagebox.showerror("DB Error", "Cannot Connect to Database" )
    logger.exception("Cannot connect to Database")




def get_Quote():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select * from Magic_Quotes where Theme_ID = 1"
    cur.execute(sql)
    rows = cur.fetchone()

    connection.commit()
    connection.close()
    return rows[1]
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")

def get_Running_Notes():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select Title_Running_Notes, Title_Notes_Language from Magic_Science_Lessons where Lesson_ID = ?"
    cur.execute(sql, (TEST_ROW, ))
    qret = cur.fetchone()
    text = qret[0]
    language = qret[1]

    print(language+text)
    connection.commit()
    connection.close()
    return (text, language)
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")






#get_Quote()
def class_info():
 try:
    list_names = []
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = "select * from Magic_Class_Info"
    cur.execute(sql)
    rows = cur.fetchall()
    for element in rows:
        list_names.append(element)
    connection.commit()
    connection.close()
    return list_names
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")


def get_factual_content():
 try:
    list_factual_content = []
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = ('select Factual_Term1, Factual_Term1_Description, Factual_Term2, Factual_Term2_Description, Factual_Term3'
          ', Factual_Term3_Description, Factual_Image1, Factual_Image2, Factual_Image3 from Magic_Science_Lessons where Lesson_ID = ?')
   # sql = 'select Factual_Term1, Factual_Term1_Description, Factual_Term2, Factual_Term2_Description, Factual_Term3, from Magic_Science_Lessons where Lesson_ID=TEST_ROW'
    factual_info_c = cur.execute(sql,(TEST_ROW,))
    factual_info = factual_info_c.fetchone()
   # print(factual_info)
    factual_terms = [factual_info[0], factual_info[2], factual_info[4]]
    factual_descriptions = [factual_info[1], factual_info[3], factual_info[5]]
    factual_images = [imageroot+factual_info[6], imageroot+factual_info[7], imageroot+factual_info[8]]
    connection.close()
    return (factual_terms, factual_descriptions, factual_images)
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")


def get_experiment_content():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()

    sql = ('select Application_Steps_Number, Application_Step_Description_1, Application_Step_Description_2, Application_Step_Description_3,'
        'Application_Step_Description_4,Application_Step_Description_5,Application_Step_Description_6,Application_Step_Description_7'
        ',Application_Step_Description_8,Application_Steps_Widget_1,Application_Steps_Widget_2,Application_Steps_Widget_3,Application_Steps_Widget_4'
        ',Application_Steps_Widget_5,Application_Steps_Widget_6,Application_Steps_Widget_7,Application_Steps_Widget_8 from Magic_Science_Lessons '
        'where Lesson_ID = ?')
    experiment_info_c = cur.execute(sql, (TEST_ROW,))
    experiment_info = experiment_info_c.fetchone()
    #print(experiment_info)
    experiment_steps = [experiment_info[1], experiment_info[2], experiment_info[3],experiment_info[4],experiment_info[5],experiment_info[6],experiment_info[7],experiment_info[8]]
    experiment_images = [imageroot+experiment_info[9], imageroot+experiment_info[10], imageroot+experiment_info[11],imageroot+experiment_info[12],imageroot+experiment_info[13],imageroot+experiment_info[14],imageroot+experiment_info[15],imageroot+experiment_info[16]]
    experiment_steps_total = experiment_info[0]
    connection.close()
    return experiment_steps, experiment_images, experiment_steps_total
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")


def get_application_video():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = 'select Application_Video_Link, Application_Video_Running_Notes from Magic_Science_Lessons where Lesson_ID=?'
    video_info_c = cur.execute(sql, (TEST_ROW,))
    video_info = video_info_c.fetchone()
    f = open("demofile3.txt", "w")
    f.write("Woops! I have deleted the content!"+video_info[1])
    f.close()
    video_link = videoroot+video_info[0]
    connection.close()
    return (video_link,video_info[1])
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")


def get_ip_data():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = 'select Answer_Key,IP_Questions, Lesson_ID, NumberOfQuestions from Magic_Science_Lessons where Lesson_ID=?'
    ip_info_c = cur.execute(sql, (TEST_ROW,))
    ip_info = ip_info_c.fetchone()
    connection.close()
    return ip_info
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")

def get_application_mode():
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()
    sql = 'select Application_Mode from Magic_Science_Lessons where Lesson_ID=?'
    ap_info_c = cur.execute(sql, (TEST_ROW,))
    ap_info = ap_info_c.fetchone()[0]
    connection.close()
    return ap_info
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")


def save_leader_board_data(list_points):
 try:
    connection = sqlite3.connect(db)
    cur = connection.cursor()

    for element in list_points:
        sql = "select Badge_A_Threshold, Badge_B_Threshold, Badge_C_Threshold from Magic_Class_Info where Name=?"
        badge_info_c = cur.execute(sql, (element[0],))
        badge_info = badge_info_c.fetchone()
        badge_a = badge_info[0]
        badge_b = badge_info[1]
        badge_c= badge_info[2]
        var = StringVar()
        var = element[1]
        value = var.get()
        badge = ''
        if int(value) > badge_a:
            badge = 'a'
        elif int(value) > badge_b:
            badge ='b'
        elif int(value) > badge_c:
            badge = 'c'
        if int(value) >=100:
            value = str(99)
        sql='update Magic_Class_Info set Points = ? , Badge = ? where Name=?'
        print(value,element[0])
        cur.execute(sql,(int(value), badge, element[0]))

    connection.commit()
    connection.close()
 except sqlite3.OperationalError:
     messagebox.showerror("DB Error", "Cannot Connect to Database")
     logger.exception("Cannot connect to Database")
