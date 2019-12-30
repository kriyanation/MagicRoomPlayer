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
   # sql = 'select Factual_Term1, Factual_Term1_Description, Factual_Term2, Factual_Term2_Description, Factual_Term3, from Magic_Science_Lessons where Lesson_ID=5'
    factual_info_c = cur.execute(sql,(5,))
    factual_info = factual_info_c.fetchone()
    print(factual_info)
    factual_terms = [factual_info[0], factual_info[2], factual_info[4]]
    factual_descriptions = [factual_info[1], factual_info[3], factual_info[5]]
    factual_images = [factual_info[6], factual_info[7], factual_info[8]]
    connection.close()
    return (factual_terms, factual_descriptions, factual_images)
