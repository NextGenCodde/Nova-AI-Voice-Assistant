import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import datetime
from openai import OpenAI
from gtts import gTTS
import pygame.display
import os
import subprocess
import threading

# from elevenlabs import ElevenLabs, Voice, VoiceSettings, play
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
#for ui 
import tkinter as tk
import ttkbootstrap as ttk
# from tkinter import ttk
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# # Function to speak the given text
# def speak_old(text):
#     engine.say(text)
#     engine.runAndWait()

#google text


client = ElevenLabs(
  api_key='sk_20b1a5899d669aed061c48e8242efd55f43abf2445bfd0f3',
)



def speak(text):
    
    audio_stream = client.text_to_speech.convert_as_stream(
    text=text,
    voice_id="2EiwWnXFnvU5JabPnv8n",
    model_id="eleven_multilingual_v2"
)
# Save stream to file
    with open("output.mp3", "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    # Play audio using pygame
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
     pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove('output.mp3')
     




# def speak_old(text):
#     temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp.mp3')
#     tts = gTTS(text)
#     tts.save(temp_file)
#     # Rest of your function remains the same
#     pygame.mixer.init()
#     pygame.mixer.music.load(temp_file)
#     pygame.mixer.music.play()

#     while pygame.mixer.music.get_busy():
#       pygame.time.Clock().tick(10)
      
#     pygame.mixer.music.unload()
#     os.remove(temp_file)
# OpenAI DeepSeek Chat Function
# Store chat history globally
conversation_history = [
    {"role": "system", "content": "You are a helpful AI assistant named Nova. Give short or specific responses."}
]

def deepseek_chat(command):
    global conversation_history  # Use the global chat history

    client = OpenAI(
        base_url="https://api.novita.ai/v3/openai",
        api_key="sk_Qs6ZALHnkKSl-wXf1Uc2EZ5NxBk7ZphmOYctkNkBOco",
    )

    model = "meta-llama/llama-3.1-8b-instruct"
    max_tokens = 512

    # Add the new user input to conversation history
    conversation_history.append({"role": "user", "content": command})

    # Limit history to avoid large payloads
    if len(conversation_history) > 10:
        conversation_history.pop(1)  # Remove old messages except system message

    chat_completion_res = client.chat.completions.create(
        model=model,
        messages=conversation_history,
        max_tokens=max_tokens,
    )

    response = chat_completion_res.choices[0].message.content

    # Add AI response to conversation history
    conversation_history.append({"role": "assistant", "content": response})

    return response

# Function to get weather information

# Process user commands
def processcommand(c):
    c = c.lower()
    global text_output  # Ensure text_output is accessible
    #open any website
    if c.startswith("open"):
        web = c.split(" ")[1]
        webbrowser.open(f'https://{web}.com')
        speak(f"opening {web}")
        window.after(0, lambda: text_output.insert(tk.END, f"Nova: opening {web}\n"))
    # Play music from the library
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
        speak(f"Playing {song}")
        window.after(0, lambda: text_output.insert(tk.END, f"Nova: Playing {song}\n"))

    # Search Google
    elif c.startswith("search for"):
        query = c.replace("search for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak(f"Searching Google for {query}")
        window.after(0, lambda: text_output.insert(tk.END, f"Nova: Searching Google for {query}\n"))

    # Search YouTube
    elif c.startswith("search youtube for"):
        query = c.replace("search youtube for", "").strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        speak(f"Searching YouTube for {query}")
        window.after(0, lambda: text_output.insert(tk.END, f"Nova: Searching YouTube for {query}\n"))

    # Get weather information
    elif c.startswith("what's the weather in"):
        city = c.replace("what's the weather in", "").strip()
        webbrowser.open(f"https://www.google.com/search?q=weather+in+{city}")
        speak(f"Searching for weather in {city}")
        window.after(0, lambda: text_output.insert(tk.END, f"Nova: Searching for Weather in {city}\n"))

    # Get current time
    elif "what time is it" in c or "current time" in c or 'tell me time' in c:
        now = datetime.datetime.now().strftime("%I:%M %p")
        window.after(0, lambda: text_output.insert(tk.END, f"Nova: The current time is {now}\n"))
        speak(f"The current time is {now}")

    # Get current date
    elif "what's the date today" in c or "today's date" in c or "current date" in c or 'tell me date' in c:
        today = datetime.datetime.now().strftime("%B %d, %Y")
        window.after(0, lambda: text_output.insert(tk.END, f"Nova: Today's date is {today}\n"))
        speak(f"Today's date is {today}")
    #opeing local files or apps 
    elif 'notepad' in c:
        os.startfile("notepad.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening notpad\n"))
        speak('opening notepad')
    elif'calculator' in c:
        os.startfile("calc.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening calculator\n"))
        speak('opening calculator')
    elif'vs code' in c:
        os.startfile(r"F:\Microsoft VS Code\Code.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening vs code\n"))
        speak('opening vs code')
    elif 'cursor' in c:
        os.startfile(r"C:\Users\COmputer\AppData\Local\Programs\cursor\Cursor.exee")
        window.after(0, lambda: text_output.insert(tk.END, "opening cursor\n"))
        speak('opening cursor')
    elif 'whatsapp' in c:
        subprocess.run(["cmd", "/c", "start whatsapp:"])
        window.after(0, lambda: text_output.insert(tk.END, "opening whatsapp\n"))
        speak('opening whatsapp')
    elif 'chrome' in c or 'google' in c:
        os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening chrome \n"))
        speak('opening chrome')
    elif 'pieces' in c:
        os.startfile(r"F:\Pieces for Developers\pieces_for_x.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening pieces \n"))
        speak('opening pieces')
    elif 'microsoft edge' in c:
        os.startfile(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening microsoft edge \n"))
        speak('opening microsoft edge')
    elif 'downloads' in c:
        os.startfile(r"C:\Users\COmputer\Downloads")
        window.after(0, lambda: text_output.insert(tk.END, "opening downloads \n"))
        speak('opening download')
    elif 'desktop' in c:
        os.startfile(r"C:\Users\COmputer\Desktop")
        window.after(0, lambda: text_output.insert(tk.END, "opening desktop \n"))
        speak('opening desktop')
     # Stop listening command
    elif "stop listening" in c or "power off" in c or 'stop' in c:
        window.after(0, lambda: text_output.insert(tk.END, "Nova: Okay, I will stop listening. Goodbye!\n"))
        speak("Okay, I will stop listening. Goodbye!")
        button.config(state=tk.NORMAL) 
        text_output.insert(tk.END, "Nova has stopped. Press 'Start Listening' to restart.\n")
        return False  # This will stop the listening loop   
    # General AI chat response
    else:
        output = deepseek_chat(c)
        print(output)
        window.after(0, lambda: text_output.insert(tk.END, f"Nova: {output}\n"))
        speak(output)
    return True
 # Keep listening

# Continuous Listening Mode
def listen_continuously():
    text_output.insert(tk.END, f"Nova: Nova activated. I am listening\n")
    text_output.update_idletasks()
    speak("Nova activated. I am listening.")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                text_output.insert(tk.END, f"Nova: Listening\n")
                text_output.update_idletasks()
                audio = recognizer.listen(source , timeout=2)

            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            text_output.insert(tk.END, f"You: {command}\n")
            text_output.update_idletasks()

            if not processcommand(command):
                break  # Stop listening if user says "stop listening"

        except Exception as e:
            print(f"Error: {e}")

# Flag to stop wake word listener after detection

def mainfunc():
    global wake_word_detected
    wake_word_detected = False
    button.config(state=tk.DISABLED) 
    text_output.insert(tk.END, f"Initializing Nova \n")
    text_output.update_idletasks()  
    speak("Initializing Nova")
    
    def wake_word_listener():
        global wake_word_detected
        while not wake_word_detected:  # Run only if wake word not detected
            recognizer = sr.Recognizer()
            print("Listening for wake word...")
            text_output.insert(tk.END, f"Nova: Listening for wake word...\n")
            text_output.update_idletasks()  

            try:
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=2)

                word = recognizer.recognize_google(audio)
                print(f"Wake word detected: {word}")
                text_output.insert(tk.END, f"Wake word detected: {word}\n")
                text_output.update_idletasks()  

                if 'nova' in word.lower():
                    wake_word_detected = True  # Stop listening for wake word
                    listen_thread = threading.Thread(target=listen_continuously, daemon=True)
                    listen_thread.start()  # Start continuous listening

            except Exception as e:
                print(f"Error: {e}")

    # Start wake word listener in a separate thread
    wake_thread = threading.Thread(target=wake_word_listener, daemon=True)
    wake_thread.start()



'''
Designing the ui for Ai voice assistant
import tkinter as tk 
import tkinter as ttk provide all the widgets 
import ttkbootstrap as ttk provide all the widgets styles 
'''
# the main window 

window = ttk.Window(themename='darkly')
window.title('Nova AI Voice Assistant')
window.geometry('700x500')
# window = ttk.window()
# Add a Scrollbar for better text viewing
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text = tk.Label(master=window , text = 'NOVA' , font='Poppins 24 bold')
text.pack()


text_output = tk.Text(master=window, yscrollcommand=scrollbar.set, wrap=tk.WORD)
text_output.pack(expand=True, fill=tk.BOTH)
scrollbar.config(command=text_output.yview)  # Link scrollbar to text output




button = tk.Button(
    master=window, text='Start',command=mainfunc, 
    padx=10,  # Increase horizontal padding
    pady=10,  # Increase vertical padding
    width=15,  # Set a fixed width
    height=1,  # Set a fixed height
    font=("Arial", 14, "bold")# Increase text size
    
)
button.pack(pady=10)
# run
window.mainloop()