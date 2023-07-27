import pyttsx3
import speech_recognition as sr

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5)  # Set a timeout of 5 seconds
            print("Recognizing...")
            command = r.recognize_google(audio, language='en-in')
            print(f"You said: {command}\n")
            return command
        except sr.WaitTimeoutError:
            print("No command received. Continue listening...")
            return "None"
        except Exception as e:
            print("Error recognizing speech:", e)
            return "None"