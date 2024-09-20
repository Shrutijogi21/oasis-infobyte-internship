import speech_recognition as sr
import pyttsx3
import datetime
import wikipediaapi
import webbrowser

# Initialize the speech recognition engine
r = sr.Recognizer()

# Set the default voice for text-to-speech synthesis
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Change the index to use a different voice if needed


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet():
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        speak("Good morning!")

    elif 12 <= hour < 18:
        speak("Good afternoon!")

    else:
        speak("Good evening!")

    speak("How can I assist you?")


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            # Add timeout for no speech detected after 5 seconds
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("No speech detected. Terminating.")
            speak("No speech detected. Goodbye!")
            exit()

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"You said: {query}\n")

    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Can you please repeat?")
        return ""
    except sr.RequestError:
        print("Couldn't request results. Check your internet connection.")
        return ""

    return query


def search_web(query):
    speak(f"Searching for {query} on the web...")
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)


def execute_command(command):
    if "hello" in command:
        speak("Hello there!")

    elif 'wikipedia' in command:
        speak('Searching Wikipedia...')
        command = command.replace("wikipedia", "").strip()
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page = wiki_wiki.page(command)
        if page.exists():
            results = page.summary[:1000]  # Limit the summary length if needed
            speak('According to Wikipedia')
            print(results)
            speak(results)
        else:
            speak("Sorry, I couldn't find anything on Wikipedia.")

    elif "search" in command:
        search_query = command.split("search")[-1].strip()
        search_web(search_query)

    elif 'open youtube' in command:
        webbrowser.open("youtube.com")
        speak("Opening YouTube")
        return True  # Stop listening after opening YouTube

    elif 'open google' in command:
        webbrowser.open("google.com")
        speak("Opening Google")
        return True  # Stop listening after opening Google

    elif 'play music' in command:
        webbrowser.open("spotify.com")
        speak("Playing music on Spotify")
        return True  # Stop listening after opening Spotify

    elif 'time' in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {now}")
        print(now)

    elif 'date' in command:
        now = datetime.datetime.now().strftime("%d-%m-%Y")
        speak(f"The date is {now}")

    elif 'exit' in command:
        speak("Goodbye!")
        exit()

    else:
        speak("I'm sorry, I couldn't understand your command.")

    return False  # Continue listening if no exit conditions are met


if __name__ == "__main__":
    greet()
    while True:
        command = listen().lower()
        if command:
            stop = execute_command(command)
            if stop:
                break  # Exit the loop after executing certain commands

