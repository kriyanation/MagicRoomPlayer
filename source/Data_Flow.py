import sqlite3
import random
from tkinter import StringVar
TEST_ROW = 5
def get_Title():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = "select Lesson_Title from Magic_Science_Lessons where Lesson_ID = ?"
    cur.execute(sql, (TEST_ROW, ))
    text = cur.fetchone()[0]
    #print(text)
    connection.commit()
    connection.close()
    return text



#get_Title()

def get_title_image():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = "select Title_Image from Magic_Science_Lessons where Lesson_ID = ?"
    cur.execute(sql, (TEST_ROW, ))
    text = cur.fetchone()[0]
    print(text)
    connection.commit()
    connection.close()
    return text

def get_title_video():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = "select Title_Video from Magic_Science_Lessons where Lesson_ID = ?"
    cur.execute(sql, (TEST_ROW, ))
    text = cur.fetchone()[0]
    #print(text)
    connection.commit()
    connection.close()
    return text

get_title_image()


def get_Quote():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = "select count(*) from Magic_Quotes"
    cur.execute(sql)
    rows = cur.fetchall()
    list_names = []
    for element in rows:
        list_names.append(element)


    for element in list_names:
        count = int(element[0])
    # print(str(count)+"count")
    q_text_number = random.randint(1, count)
    cur = connection.cursor()
    sql = "select * from Magic_Quotes where Theme_ID = ?"
    cur.execute(sql, (q_text_number,))
    rows = cur.fetchall()
    list_quote = []
    for element in rows:
        list_quote.append(element)
    connection.commit()

    for element in list_quote:
        quote = element[1]
    print(quote)
    connection.commit()
    connection.close()
    return quote

def get_Running_Notes():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
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






#get_Quote()
def class_info():
    list_names = []
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = "select * from Magic_Class_Info"
    cur.execute(sql)
    rows = cur.fetchall()
    for element in rows:
        list_names.append(element)
    connection.commit()
    connection.close()
    return list_names


def get_factual_content():
    list_factual_content = []
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = ('select Factual_Term1, Factual_Term1_Description, Factual_Term2, Factual_Term2_Description, Factual_Term3'
          ', Factual_Term3_Description, Factual_Image1, Factual_Image2, Factual_Image3 from Magic_Science_Lessons where Lesson_ID = ?')
   # sql = 'select Factual_Term1, Factual_Term1_Description, Factual_Term2, Factual_Term2_Description, Factual_Term3, from Magic_Science_Lessons where Lesson_ID=TEST_ROW'
    factual_info_c = cur.execute(sql,(TEST_ROW,))
    factual_info = factual_info_c.fetchone()
   # print(factual_info)
    factual_terms = [factual_info[0], factual_info[2], factual_info[4]]
    factual_descriptions = [factual_info[1], factual_info[3], factual_info[5]]
    factual_images = [factual_info[6], factual_info[7], factual_info[8]]
    connection.close()
    return (factual_terms, factual_descriptions, factual_images)


def get_experiment_content():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()

    sql = ('select Application_Steps_Number, Application_Step_Description_1, Application_Step_Description_2, Application_Step_Description_3,'
        'Application_Step_Description_4,Application_Step_Description_5,Application_Step_Description_6,Application_Step_Description_7'
        ',Application_Step_Description_8,Application_Steps_Widget_1,Application_Steps_Widget_2,Application_Steps_Widget_3,Application_Steps_Widget_4'
        ',Application_Steps_Widget_5,Application_Steps_Widget_6,Application_Steps_Widget_7,Application_Steps_Widget_8 from Magic_Science_Lessons '
        'where Lesson_ID = ?')
    experiment_info_c = cur.execute(sql, (TEST_ROW,))
    experiment_info = experiment_info_c.fetchone()
    #print(experiment_info)
    experiment_steps = [experiment_info[1], experiment_info[2], experiment_info[3],experiment_info[4],experiment_info[TEST_ROW],experiment_info[6],experiment_info[7],experiment_info[8]]
    experiment_images = [experiment_info[9], experiment_info[10], experiment_info[11],experiment_info[12],experiment_info[13],experiment_info[14],experiment_info[15],experiment_info[16]]
    experiment_steps_total = experiment_info[0]
    connection.close()
    return experiment_steps, experiment_images, experiment_steps_total


def get_application_video():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = 'select Application_Video_Link, Application_Video_Running_Notes from Magic_Science_Lessons where Lesson_ID=?'
    video_info_c = cur.execute(sql, (TEST_ROW,))
    video_info = video_info_c.fetchone()
    connection.close()
    return video_info


def get_ip_data():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = 'select Answer_Key,IP_Questions, Lesson_ID, NumberOfQuestions from Magic_Science_Lessons where Lesson_ID=?'
    ip_info_c = cur.execute(sql, (TEST_ROW,))
    ip_info = ip_info_c.fetchone()
    connection.close()
    return ip_info

def get_application_mode():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = 'select Application_Mode from Magic_Science_Lessons where Lesson_ID=?'
    ap_info_c = cur.execute(sql, (TEST_ROW,))
    ap_info = ap_info_c.fetchone()[0]
    connection.close()
    return ap_info


def save_leader_board_data(list_points):
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
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
        sql='update Magic_Class_Info set Points = ? , Badge = ? where Name=?'
        print(value,element[0])
        cur.execute(sql,(int(value), badge, element[0]))

    connection.commit()
    connection.close()
