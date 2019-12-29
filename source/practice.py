import tkinter as tk
from tkinter import ttk
import unicodedata, unidecode

root = tk.Tk()
text = 'श्वसन प्रणाली में नाक गुहा, ट्रेकिआ और फेफड़े होते हैं'
unicodetext = '\u0936\u094D\u0935\u0938\u0928\20\u092A\u094D\u0930\u0923\u093E\u0932\u0940'
a = bytes(text , 'utf-8')
a = str(text)

text4 = unicodedata.normalize("NFC", unicodetext)
print(text4)
text1 = unicodedata.normalize('NFC', unicodetext)
text2 = unicodedata.normalize('NFD', unicodetext)
text3 = unicodedata.normalize('NFKD', unicodetext)
labelcheck = ttk.Label(text=text1, font = "Lohit\Devnagri")
textcheck = tk.Text()
textcheck.insert(tk.END, text2)
canvascheck = tk.Canvas(root,width=800, height=200)
canvascheck.create_text(200, 20, font="Lohit\ Devnagri", text=text3)
labelcheck.grid(row = 0, column = 0)
textcheck.grid(row =0, column = 1)
canvascheck.grid(row = 1, column =0)
print(text)
root.mainloop()