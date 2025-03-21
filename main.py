import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import music_library
import google.generativeai as genai
import datetime
import os


recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = os.getenv("63e31991c3d45da9efa111aed15e1c1") 

def speak(text):
    engine.say(text)
    engine.runAndWait()


def aiProcess(command):
    genai.configure(api_key="AIzaSyCxGm_EFvP3GCPs2xS6E806ck2G_RHB_uw")

    model = genai.GenerativeModel("gemini-1.5-flash")
    

    chat = model.start_chat(history=[
        {"role": "user", "parts": [{"text": "what is coding"}]},
        {"role": "model", "parts": [{"text": "You are a virtual assistant named Jarvis, skilled in general tasks."}]}
    ])

    response = chat.send_message(command)  
    return response.text




def processCommand(command):
    command = command.lower()
    
    if "open" in command:
        words = command.split()
        for word in words:
            if "." in word: 
                url = f"https://{word}"
                webbrowser.open(url)
                return

        website_name = words[-1]  
        url = f"https://{website_name}.com"
        webbrowser.open(url)

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}")

    elif command.startswith("play"):
        song = command.split(" ")[1]
        try:
            link = music_library.music[song]
            webbrowser.open(link)
        except KeyError:
            speak("Song not found in library.")

    elif "news" in command:
        if not newsapi:
            speak("News API key is missing.")
            return
        
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            for article in articles[:5]: 
                speak(article["title"])
        else:
            speak("Unable to say news.")

    else:
        output = aiProcess(command)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis....")
    
    while True:
        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                word = recognizer.recognize_google(audio)
                print(f"Recognized: {word}")

            if "jarvis" in word.lower():
                speak("Yes sir")
                
                with sr.Microphone() as source:
                    print("Jarvis Active, Listening...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=7)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    
                    processCommand(command)

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except Exception as ex:
            print(f"Error: {ex}")
