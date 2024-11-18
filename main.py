import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTs
import pygame
import os
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "563e31991c3d45da9efa111aed15e1c1"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTs(text)
    tts.save('temp.mp3')
    
    # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("yourfile.mp3")

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running while the music is playing
    while pygame.mixer.music.get_busy():  
        pygame.time.Clock().tick(10) 

    pygame.mixer.music.unload()
    os.remove("temp.mp3")


def aiprocess(command):
    client = OpenAI(api_key="sk-proj--Wx17ehGk2PnwmzCHcDwT3BlbkFJMj6bYTk9jG1bqZaFTcj",
    )

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short reponses please"},
        {"role": "user", "content": "Command"}
    ]
    )

    return completion.choices[0].message.content

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif c.lower().startwith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link) 

    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=API_KEY")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            # Print the headlines
            for article in articles:
                speak(article['title'])
                 
    else:
        # Let OpenAI handle the request
        output = aiprocess(c)
        speak(output)




if __name__ == "__main__":
    speak("Initializing jarvis....")
    while True: 
        # Listen for the wake word "Jarvis"  
        # obtain audio from the microphone
        r = sr.Recognizer()
        

        print("recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout = 2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Yes Sir How may I can help you")
                # listen for command 
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processcommand(command)



        except Exception as e:
            print("Error; {0}".format(e))
 
