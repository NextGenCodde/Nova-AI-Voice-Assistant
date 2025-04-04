import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import datetime
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import subprocess
import threading
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
def speak(text):
    temp_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp.mp3')
    tts = gTTS(text)
    tts.save(temp_file)
    # Rest of your function remains the same
    pygame.mixer.init()
    pygame.mixer.music.load(temp_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)
      
    pygame.mixer.music.unload()
    os.remove(temp_file)
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

    if 'open google' in c:
        webbrowser.open('https://google.com')
        speak(f'opening google')
        text_output.insert(tk.END, f"Nova: Opening Google\n")
        text_output.update_idletasks()  # Force UI update
    elif 'open youtube' in c:
        webbrowser.open('https://youtube.com')
        speak("Opening YouTube")
        text_output.insert(tk.END, f"Nova: Opening Youtube\n")
        text_output.update_idletasks()
    elif 'open facebook' in c:
        webbrowser.open('https://facebook.com')
        speak("Opening Facebook")
        text_output.insert(tk.END, f"Nova: Opening Facebook\n")
        text_output.update_idletasks()
    elif 'open linkedin' in c:
        webbrowser.open('https://linkedin.com')
        speak("Opening LinkedIn")
        text_output.insert(tk.END, f"Nova: Opening Linkedin\n")
        text_output.update_idletasks()

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

    # Stop listening command
    elif "stop listening" in c or "power off" in c or 'stop' in c:
        speak("Okay, I will stop listening. Goodbye!")
        window.after(0, lambda: text_output.insert(tk.END, "Nova: Okay, I will stop listening. Goodbye!\n"))
        return False  # This will stop the listening loop
    #opeing local files or apps 😍
    elif "open notepad" in c or 'notepad' in c:
        os.startfile("notepad.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening notpad\n"))
        speak('opening notepad')
    elif "open calculator" in c or 'notepad' in c:
        os.startfile("calc.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening calculator\n"))
        speak('opening calculator')
    elif 'open vs code' in c or 'vs code' in c:
        os.startfile(r"F:\Microsoft VS Code\Code.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening vs code\n"))
        speak('opening vs code')
    elif 'open cursor' in c or 'cursor' in c:
        os.startfile(r"C:\Users\COmputer\AppData\Local\Programs\cursor\Cursor.exee")
        window.after(0, lambda: text_output.insert(tk.END, "opening cursor\n"))
        speak('opening cursor')
    elif 'whatsapp' in c:
        subprocess.run(["cmd", "/c", "start whatsapp:"])
        window.after(0, lambda: text_output.insert(tk.END, "opening whatsapp\n"))
        speak('opening whatsapp')
    elif 'open chrome' in c or 'chrome' in c:
        os.startfile(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening chrome \n"))
        speak('opening chrome')
    elif 'open pieces' in c or 'pieces' in c:
        os.startfile(r"F:\Pieces for Developers\pieces_for_x.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening pieces \n"))
        speak('opening pieces')
    elif 'open microsoft edge' in c or 'microsoft edge' in c:
        os.startfile(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
        window.after(0, lambda: text_output.insert(tk.END, "opening microsoft edge \n"))
        speak('opening microsoft edge')
    elif 'open downloads' in c or 'downloads' in c:
        os.startfile(r"C:\Users\COmputer\Downloads")
        window.after(0, lambda: text_output.insert(tk.END, "opening downloads \n"))
        speak('opening download')
    elif 'open desktop' in c or 'desktop' in c:
        os.startfile(r"C:\Users\COmputer\Desktop")
        window.after(0, lambda: text_output.insert(tk.END, "opening desktop \n"))
        speak('opening desktop')
        

        
    # General AI chat response
    else:
        output = deepseek_chat(c)
        print(output)
        window.after(0, lambda: text_output.insert(tk.END, f"Nova: {output}\n"))
        speak(output)

    return True  # Keep listening
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
                audio = recognizer.listen(source)

            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            text_output.insert(tk.END, f"You: {command}\n")
            text_output.update_idletasks()

            if not processcommand(command):
                break  # Stop listening if user says "stop listening"

        except Exception as e:
            print(f"Error: {e}")

# Flag to stop wake word listener after detection
wake_word_detected = False

def mainfunc():
    global wake_word_detected
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
    master=window, text='Start Listening',command=mainfunc, 
    padx=10,  # Increase horizontal padding
    pady=10,  # Increase vertical padding
    width=15,  # Set a fixed width
    height=1,  # Set a fixed height
    font=("Arial", 14, "bold")# Increase text size
    
)
button.pack(pady=10)
# run
window.mainloop()