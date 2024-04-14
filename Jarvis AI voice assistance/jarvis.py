import pyttsx3 
import speech_recognition
import requests
from bs4 import BeautifulSoup
import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton
from dialog_ui import Ui_Dialog

from PyQt5.QtWidgets import QApplication, QMainWindow

act = []

# load ui
class MyGui(QMainWindow,QDialog):
    def __init__(self):
        super(MyGui, self).__init__()
        uic.loadUi('form.ui', self)
        self.start.clicked.connect(self.start_clicked)
        self.end.clicked.connect(self.exit_clicked)
        self.show()
        
    def start_clicked(self):
        print("clicked")
        self.dialog = QDialog()  # Create an instance of QDialog
        self.ui = Ui_Dialog()  # Create an instance of the generated UI class
        self.ui.setupUi(self.dialog)  # Set up the UI inside the QDialog
        # self.ui.speak.hide()
        
        
        # build engine
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 150)
        self.dialog.show()  # Show the dialog window
        self.listen_for_commands(self.engine)
        

    def listen_for_commands(self, engine):
        while True:
            query = self.takeCommand().lower()
            if act[-1] == 'list':
                self.ui.listen.show()
                self.ui.speak.hide()
            if "wake up" in query :
                from greetMe import greetme
                greetme()

                while True:
                    query = self.takeCommand().lower()
                    if 'go to sleep' in query:
                        self.speak('Jarvis going to sleep..')
                        sys.exit()
                        break
                        
                    ## conversation
                    if 'who is your developer' in query:
                        self.speak('my developer is Fatima, she is a skilled AI developer. she created several AI projects including chatbots, computer vision, object detection, deep learning and voice assistants like me, You can contact here anytime to place an order ')
                    if ('hello' in query) or ('hi' in query) or ('hey' in query):
                        self.speak('Hello! Hope you are good, is there anything i can help you with?')
                    if 'how are you' in query:
                        self.speak("I'm good, how are you?")
                    if ('i am good' in query) or ('i am fine' in query):
                        self.speak('Good to hear that you are fine. How can I assist you today?')
                    elif ('i am not good' in query) or ('i am not fine' in query) or ('i am feeling low' in query):
                        self.speak('Sad to hear that, how cani make your day better?')

                    ## searching
                    elif ('search' in query)  and ('google' in query):
                        from search import search_google
                        search_google(query)
                    elif (('search' in query) or('play' in query))  and ('youtube' in query):
                        from search import search_yt
                        search_yt(query)

                    elif 'what is the temperature' in query:
                        search = 'temperature in karachi'
                        place = 'karachi'
                        if 'in' in query:
                            place = query.split('in')[1]
                            search = 'temperature in '+place
                        url = 'https://www.google.com/search?q=' + search
                        page = requests.get(url)
                        soup = BeautifulSoup(page.text, 'html.parser')
                        temp = soup.findAll('div', {'class': 'BNeawe iBp4i AP7Wnd'})[1].text
                        self.speak(f'The current temperature in {place} is {temp}.')
                    elif 'what is the weather' in query or ('tell' in query and 'weather' in query):
                        search = 'weather in karachi'
                        place = 'karachi'
                        if 'in' in query:
                            place = query.split('in')[1]
                            search = 'weather in '+place
                        url = 'https://www.google.com/search?q=' + search
                        page = requests.get(url)
                        soup = BeautifulSoup(page.text, 'html.parser')
                        weath = soup.find('div', {'class': 'BNeawe tAd8D AP7Wnd'}).text
                        self.speak(f'The current weather in {place} on {weath}.')
                    elif ('what' in query or 'tell' in query) and ('time' in query)  :
                        t = datetime.datetime.now().strftime('%H:%M')
                        self.speak('The time in  Karachi is %s.' %t )

    def takeCommand(self):
        r = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            act.append('list')
            print("Listening...")
          
            print(act)
            r.pause_threshold = 1  # pause a little to lstn
            r.energy_threshold = 300 # listens to voice of 300 energy threshold
            audio = r.listen(source, 0 ,4) # waits 4 seconds to listen

        try:
            print("Understanding...")
            query = r.recognize_google(audio, language = 'en-in')
            act.append('speak')
            print(act)

            print(f"You said : {query}\n")
        except Exception as e:
            self.speak("Say that again please..")  
            return 'None'
        return query
        
    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def exit_clicked(self):
        print('exit')
        sys.exit()  
    



if __name__ == "__main__":
    # run app 
    app = QApplication([])
    window = MyGui()
    app.exec_()
