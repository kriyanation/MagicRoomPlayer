
from reportlab.pdfgen import canvas
import Data_Flow,pyttsx3
try:
    import pypiwin32
except ImportError:
    print("pypiwin32 not available")

import shutil,os
import subprocess
import tkinter as tk


def animate_text(frame, text, counter, textwidget, counter_max):
    #print(text)
    textwidget.insert(float(counter+1),text[counter])
    if counter >= counter_max:
        # self.playtextsound(quote_text)
        textwidget.configure(state="disabled")
        return
    frame.after(100, lambda: animate_text(frame, text, counter + 1, textwidget, counter_max))


def playtextsound(text,V='m',L='en'):
    engine = pyttsx3.init(driverName='espeak')
    engine.setProperty('voice', 'en+f2')
    engine.setProperty('rate', 130)
    engine.setProperty("volume",0.9)
    engine.say(text)
  #  engine.say(text)
    engine.runAndWait()
   # voiceoutput = subprocess.check_output('espeak-ng -s150 -v'+L+'+f2 \"'+text+'\"',shell=True)
   # print("sound"+str(voiceoutput))



def generate_ip_paper(lesson_id,imageroot):
    text_id = Data_Flow.get_ip_data()
    text = text_id[1]
    id = text_id[2]
    cc = canvas.Canvas(imageroot+"Question_Papers/ip"+str(id)+".pdf")
    cc.setFont("Helvetica", 16)
    cc.drawCentredString(300,820,"A Learning Assessment for "+str(id))
    cc.setFont("Helvetica", 10)
    textobject = cc.beginText()
    textobject.setTextOrigin(50, 800)
    textobject.textLines(text)
    cc.drawText(textobject)
    cc.showPage()
    cc.save()
    return "ip"+str(id)+".pdf"

def generate_ip_sheets(lesson_id):
    text_id = Data_Flow.get_ip_data()
    answer_key = text_id[0]
    id = text_id[2]
    number_of_questions=text_id[3]
    qindex = 0
    answer_list=answer_key.split(",")

    class_info = Data_Flow.class_info()
    os.mkdir("../AnswerSheets/tmp")

    for element in class_info:
        ip_sheet = canvas.Canvas("../AnswerSheets/ip" + str(id) + element[0]+".pdf")
        xvalue =0
        yvalue = 800
        ip_sheet.setFont("Helvetica",16)
        ip_sheet.drawCentredString(300,810,element[0]+" Lesson ID "+str(id))
        for qindex in range(number_of_questions):
            yvalue -= 100
            xvalue = 0
            for aindex in range(4):
             #   qr = qrtools.QR(data = "Name="+element[0]+",Lesson_ID="+str(id)+"Answer="+str(qindex+1)+str(aindex+1)+"Correct="+answer_list[qindex])
                image_name = "../AnswerSheets/tmp/qrcode"+element[0]+str(aindex)+str(qindex)+".png"
              #  qr.encode(image_name)
                xvalue += 120
                ip_sheet.drawImage(image_name, xvalue,yvalue,width=80,height=80)
                ip_sheet.drawString(xvalue+30,yvalue-15,str(aindex+1))
                ip_sheet.rect(xvalue+23,yvalue-18,20,18)


        ip_sheet.showPage()
        ip_sheet.save()
    shutil.rmtree("../AnswerSheets/tmp/")


if __name__ == "__main__":
    generate_ip_sheets(5)





