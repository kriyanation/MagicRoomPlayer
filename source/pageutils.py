import pyttsx3

def animate_text(frame, text, counter, label, counter_max):
    #print(text)
    label.config(text=text[:counter])
    if counter > counter_max:
        # self.playtextsound(quote_text)
        return
    frame.after(100, lambda: animate_text(frame, text, counter + 1, label, counter_max))


def playtextsound(text,V='m'):
    engine = pyttsx3.init(driverName='espeak')
    engine.setProperty('voice', 'english+'+V+'2')
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()