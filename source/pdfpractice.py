from reportlab.pdfgen import canvas
import Data_Flow


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('cat', 'Kavivanar-Regular.ttf'))

text_id = Data_Flow.get_ip_data()
text = text_id[1]
id = text_id[2]
cc = canvas.Canvas("hello.pdf")
cc.setFont("cat", 16)
cc.drawCentredString(300,820,"மிதக்கும் பாத்திரத்தின் கீழே, மின்னும் பிறையாக பூமி மின்னிக்கொண்டிருந்தது."+str(id))
cc.setFont("cat", 10)
textobject = cc.beginText()
textobject.setTextOrigin(50, 800)
textobject.textLines(text)
cc.drawText(textobject)
cc.showPage()
cc.save()





