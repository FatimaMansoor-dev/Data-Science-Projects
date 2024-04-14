import pyttsx3 
import speech_recognition
import pywhatkit

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1  # pause a little to lstn
        r.energy_threshold = 300 # listens to voice of 300 energy threshold
        audio = r.listen(source, 0 ,4) # waits 4 seconds to listen

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language = 'en-in')
        print(f"You said : {query}\n")
    except Exception as e:
        print("Say that again please..")  
        return 'None'
    return query

def search_google(query):
    import wikipedia as googleScrap
    query = query.replace('jarvis', '')
    query = query.replace('search', '')
    try:
        pywhatkit.search(query)
        speak('this is what i found..')
        result = googleScrap.summary(query, sentences=2)
    except:
        result = f"I couldn't find anything related to {query}."
    speak(result)

def search_yt(query):
    import webbrowser
    query = query.replace('play', '')
    query = query.replace('search', '')
    web = 'https://www.youtube.com/results?search_query=' + query
    webbrowser.get().open(web)
    pywhatkit.playonyt(query)
    speak('Playing video on YouTube')
