import pyttsx3
import pyaudio
import speech_recognition as sr
import wikipedia
import webbrowser
import datetime
import os
import pyautogui
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox
from threading import Thread

# Initialize the pyttsx3 engine for speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

for i, voice in enumerate(voices):
    print(f"Voice {i}: {voice.name}")

    engine.setProperty('voice', voices[1].id)

def wish():
    hour = int(datetime.datetime.now().hour)
    if (hour >= 0 and hour < 12):
        speak("Good morning")
    elif (hour >= 12 and hour < 18):
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("How can I help you?")



def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User said: {query}")
    except Exception as e:
        print("Sorry, I could not understand. Could you please say that again?")
        return "None"
    return query.lower()

# Handle query-based actions
def handle_query(query):
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak(f"According to Wikipedia: {results}")

    elif 'open' in query:
        websites = {
            "youtube": "https://youtube.com",
            "google": "https://google.com",
            "wikipedia": "https://wikipedia.com",
            "lead code": "https://leetcode.com",
            "greek for greek": "https://www.geeksforgeeks.org",
            "stack overflow": "https://stackoverflow.com",
            "chat gpt":"https://chatgpt.com"
        }
        for site, url in websites.items():
            if f"open {site}" in query:
                speak(f"Opening {site}...")
                webbrowser.open(url)
    
    
        apps=[["vs code","C:\\Users\\Dell\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"],
              ["brave","C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Brave.lnk"],
              ["whatsapp","C:\\Users\\Dell\\Desktop\\WhatsApp.lnk"],
              ["camera","C:\\Users\\Dell\\Desktop\\Camera.lnk"],
              ["calculator","C:\\Users\\Dell\\Desktop\\Calculator.lnk"]]
        for app in apps:
            if(f"open {app[0]}".lower() in query.lower()):
                speak(f"opening {app[0]} ...")
                codepath=app[1]
                os.startfile(codepath) 

    elif 'time' in query:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {time}")

    elif 'increase volume' in query:
        pyautogui.press('volumeup')

    elif 'decrease volume' in query:
        pyautogui.press('volumedown')

    elif 'mute volume' in query:
        pyautogui.press('volumemute')

    elif 'temperature' in query:
        speak(get_temperature())

def get_temperature():
    try:
        url = "https://www.google.com/search?q=temperature"
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp = data.find("div", class_="BNeawe iBp4i AP7Wnd").text
        return f"Current temperature is {temp}"
    except Exception as e:
        return "Sorry, I couldn't fetch the temperature."

# Function to handle voice command listening in a separate thread
def listen():
    while True:
        query = takecommand()
        if query != "None":
            handle_query(query)

# Start listening in a background thread
def start_listening_thread():
    thread = Thread(target=listen)
    thread.daemon = True
    thread.start()

# GUI Setup
def update_gui(response):
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, response)
    speak(response)

# Create the main application window
root = tk.Tk()
root.title("Virtual Assistant")
root.geometry("600x400")

label = tk.Label(root, text="Click to Start Listening", font=("Arial", 16))
label.pack(pady=20)

text_output = tk.Text(root, height=10, width=70, wrap=tk.WORD)
text_output.pack(pady=10)

listen_button = tk.Button(root, text="Start Listening", font=("Arial", 14), command=start_listening_thread)
listen_button.pack(pady=10)

# Initialize the assistant and wish the user on startup
wish()

# Start the GUI loop
root.mainloop()
