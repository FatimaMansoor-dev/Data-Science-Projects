import pyttsx3 
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetme():
    hour = int(datetime.datetime.now().hour)
    if 12>=hour>=4:
        speak("Good morning!")
    elif 5>hour>12:
        speak("Good Afternoon!")
    elif 7>hour>5:
        speak('Good Evening!')
    else:
        speak('Hello')
    speak('how may i help you?')