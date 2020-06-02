


import Data_Flow_Player
import pyttsx3
import sys

try:
    import pypiwin32
except ImportError:
    print("pypiwin32 not available")

import shutil,os


_isLinux = sys.platform.startswith('linux')
if not _isLinux:
    import pythoncom
def animate_text(frame, text, counter, textwidget, counter_max):
    #print(text)


    if counter >= counter_max:
        # self.playtextsound(quote_text)
        textwidget.configure(state="disabled")
        return
    textwidget.insert(float(counter + 1), text[counter])
    frame.after(100, lambda: animate_text(frame, text, counter + 1, textwidget, counter_max))


def playtextsound(text,V='m',L='en'):
    if _isLinux:
        engine = pyttsx3.init(driverName='espeak')
    else:
        pythoncom.CoInitialize()
        engine = pyttsx3.init()
    engine.setProperty('voice', 'en+f2')
    engine.setProperty('rate', 130)
    engine.setProperty("volume",0.9)
    if text != "" and text is not None:
        engine.say(text)
        engine.runAndWait()
    else:
        return










