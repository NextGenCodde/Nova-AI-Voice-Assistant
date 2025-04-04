import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import datetime
from openai import OpenAI
from gtts import gTTS
import pygame
import os
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# # Function to speak the given text
# def speak_old(text):
#     engine.say(text)
#     engine.runAndWait()
def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')
    # Load MP3 file
    pygame.mixer.init()

    pygame.mixer.music.load('temp.mp3')
    
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)
      
    pygame.mixer.music.unload()
    os.remove('temp.mp3')
# OpenAI DeepSeek Chat Function
def deepseek_chat(command):
    client = OpenAI(
        base_url="https://api.novita.ai/v3/openai",
        api_key="sk_Qs6ZALHnkKSl-wXf1Uc2EZ5NxBk7ZphmOYctkNkBOco",
    )

    model = "meta-llama/llama-3.1-8b-instruct"
    stream = False
    max_tokens = 512

    chat_completion_res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant name nova. Give short or specific responses."},
            {"role": "user", "content": command},
        ],
        stream=stream,
        max_tokens=max_tokens,
    )

    return chat_completion_res.choices[0].message.content

# Function to get weather information

# Process user commands
def processcommand(c):
    c = c.lower()

    if 'open google' in c:
        webbrowser.open('https://google.com')
        speak("Opening Google")
    elif 'open youtube' in c:
        webbrowser.open('https://youtube.com')
        speak("Opening YouTube")
    elif 'open facebook' in c:
        webbrowser.open('https://facebook.com')
        speak("Opening Facebook")
    elif 'open linkedin' in c:
        webbrowser.open('https://linkedin.com')
        speak("Opening LinkedIn")
    
    # Play music from the library
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
        speak(f"Playing {song}")

    # Search Google
    elif c.startswith("search for"):
        query = c.replace("search for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}")

    # Search YouTube
    elif c.startswith("search youtube for"):
        query = c.replace("search youtube for", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        speak(f"Searching YouTube for {query}")

    # Google Search
    elif c.startswith("tell me about"):
           query = c.replace("tell me about", "").strip()
           webbrowser.open(f"https://www.google.com/search?q={query}")
           speak(f"Searching Google for {query}")

    # Get weather information
    elif c.startswith("what's the weather in"):
        city = c.replace("what's the weather in", "").strip()
        webbrowser.open(f"https://www.google.com/search?q=weather+in+{city}")
        speak(f"Searching for weather in {city}")

    # Get current time
    elif "what time is it" in c or "current time" in c:
        now = datetime.datetime.now().strftime("%I:%M %p")
        print(f"The current time is {now}")
        speak(f"The current time is {now}")

    # Get current date
    elif "what's the date today" in c or "today's date" in c:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        print(f"Today's date is {today}")
        speak(f"Today's date is {today}")
        

    # Stop listening command
    elif "stop listening" in c or "power off" in c or 'stop' in c:
        speak("Okay, I will stop listening. Goodbye!")
        return False  # This will stop the listening loop

    # General AI chat response
    else:
        output = deepseek_chat(c)
        print(output)
        speak(output)

    return True  # Keep listening

# Continuous Listening Mode
def listen_continuously():
    speak("Nova activated. I am listening.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            if not processcommand(command):
                break  # Stop listening if user says "stop listening"

        except Exception as e:
            print(f"Error: {e}")

def mainfunc():
    # Main Program
        if __name__ == "__main__":
            speak("Initializing Nova")
            
            while True:
                recognizer = sr.Recognizer()
                print("Listening for wake word...")

                try:
                    with sr.Microphone() as source:
                        audio = recognizer.listen(source, timeout=2)

                    word = recognizer.recognize_google(audio)
                    print(f"Wake word detected: {word}")


                    if word.lower() == 'nova':
                        listen_continuously()  # Start continuous listening

                except Exception as e:
                    print(f"Error: {e}")




mainfunc()