"""✅ SETUP INSTRUCTIONS:
1. Install required Python libraries:
   pip install SpeechRecognition pyttsx3 wikipedia requests

2.  If you're using a custom `musiclibrary.py`:
   - Create a `musiclibrary.py` file in the same directory.
   - Define a dictionary like this:
     music = {
         "songname": "https://link_to_song",
         "another song": "https://another_link"
     }

3. This script uses News API to fetch top headlines.
   - Sign up at https://newsapi.org/ to get a free API key.
   - Replace `news_api_key` in the code with your key.

🎤 USAGE INSTRUCTIONS – SAY ANY OF THE FOLLOWING COMMANDS:

🔎 Basic Conversations:
- "Hello" – Get a friendly response.
- "What time is it" / "Tell me the time"

🌐 Open Websites:
- "Open Google"
- "Open YouTube"
- "Open Facebook"
- "Open LinkedIn"

🎵 Music Playback:
- "Play songname" – Plays the song if found in `musiclibrary.py`.

📰 News:
- "Tell me the news" – Reads top 5 news headlines from News API.

📚 Wikipedia:
- "Wikipedia [topic]" – Reads a short summary about the topic from Wikipedia.

🖥️ Launch Applications (Windows only):
- "Launch notepad"
- "Launch calculator"
- "Launch paint"
- "Launch file explorer"
- "Launch command prompt"
- "Launch Microsoft Edge"

❌ Exit:
- "Exit" or "Bye" – Closes the assistant.

⚠️ NOTES:
- Speak clearly and wait for the assistant to process your voice.
- If the assistant doesn’t understand, it will ask you to repeat.
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import os
from datetime import datetime
import musiclibrary
import requests
# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
news_api_key = "news_api_key"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return None

def open_website(command):
    if "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "facebook" in command:
        speak("Opening facebook")
        webbrowser.open("https://www.facebook.com")
    elif "linkedin" in command:
        speak("Opening linkedin")
        webbrowser.open("https://www.linkedin.com")
    elif command.startswith("play"):
        song = command.split(" ")[1]  # Extract song name correctly
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    else:
        speak("Sorry, I can't open that site.")

def tell_time():
    now = datetime.now().strftime("%I:%M %p")
    speak(f"The time is {now}")

def search_wikipedia(command):
    try:
        query = command.replace("wikipedia", "").strip()
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError:
        speak("There are multiple results. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find anything on Wikipedia.")

def open_application(command):
    if "notepad" in command:
        speak("opening notepad")
        os.system("notepad")
    elif "calculator" in command:
        speak("opening calculator")
        os.system("calc")
    elif "paint" in command:
        speak("opening paint")
        os.system("mspaint")
    elif "file explorer" in command:
        speak("opening file explorer")
        os.system("explorer")
    elif "command promt" in command:
        speak("opening command promt")
        os.system("cmd")
    elif "microsoft edge" in command:
        speak("opening microsoft edge")
        os.system("start msedge")
    else:
        speak("I can't open that application.")

def greet_user():
    speak("Initializing jarvis")
    hour = datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("How can I assist you today?")

# Main program loop
greet_user()
while True:
    command = listen()
    if command:
        if "hello" in command:
            speak("Hello! How are you?")
        elif "time" in command:
            tell_time()
        elif "wikipedia" in command:
            search_wikipedia(command)
        elif "open" in command or "play" in command:
            open_website(command)
        elif "launch" in command:
            open_application(command)
        elif "news" in command:
            try:
                r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}")
                if r.status_code == 200:
                    data = r.json()
                    articles = data.get("articles", [])

                    speak("Here are the top news headlines.")
                    for article in articles[:5]:  # Limit to 5 headlines
                        speak(article['title'])
                else:
                    speak("Sorry, I couldn't fetch the news.")
            except Exception as e:
                speak("There was an error retrieving the news.")
                print(f"Error: {e}")
        elif "exit" in command or "bye" in command:
            speak("Goodbye! Have a great day.")
            break
        else:
            speak("I didn't understand. Can you repeat?")
