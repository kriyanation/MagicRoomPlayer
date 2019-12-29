import sqlite3
import random

def get_Title():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = "select Lesson_Title from Magic_Science_Lessons where Lesson_ID = ?"
    cur.execute(sql, (4, ))
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
    cur.execute(sql, (4, ))
    text = cur.fetchone()[0]
    print(text)
    connection.commit()
    connection.close()
    return text

def get_title_video():
    connection = sqlite3.connect("/home/ram/MagicRoom.db")
    cur = connection.cursor()
    sql = "select Title_Video from Magic_Science_Lessons where Lesson_ID = ?"
    cur.execute(sql, (4, ))
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
    cur.execute(sql, (5, ))
    qret = cur.fetchone()
    text = qret[0]
    language = qret[1]

    print(language+text)
    connection.commit()
    connection.close()
    return(text, language)






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
