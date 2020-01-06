from reportlab.pdfgen import canvas
import Data_Flow

text_id = Data_Flow.get_ip_data()
text = text_id[1]
id = text_id[2]
cc = canvas.Canvas("hello.pdf")
cc.setFont("Helvetica", 16)
cc.drawCentredString(300,820,"Science Test "+str(id))
cc.setFont("Helvetica", 10)
textobject = cc.beginText()
textobject.setTextOrigin(50, 800)
textobject.textLines(text)
cc.drawText(textobject)
cc.showPage()
cc.save()





