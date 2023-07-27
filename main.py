import time
import openai
import pyautogui 
import webbrowser
import speech_recognition as sr
from voice import speak, listen
from spotify import play_music, pause_music, next_song, play_song
from openai import chat_with_openai
import subprocess
import pyttsx3


def initialize_tts():
    engine = pyttsx3.init()
    # Get a list of available voices
    voices = engine.getProperty('voices')

    # Select the voice you want to use (change the index to select a different voice)
    # For example, to use a female voice, you can set index to 1
    index = 1
    engine.setProperty('voice', voices[index].id)

    return engine


def close_tab():
    pyautogui.hotkey('ctrl', 'w')

def tab_right():
    pyautogui.hotkey('ctrl', 'tab')
    
def tab_left():
    pyautogui.hotkey('ctrl', 'shift', 'tab')    
    
def switch_app():
    pyautogui.hotkey('alt', 'tab')
    
def home():
    pyautogui.hotkey('win', 'd')    

def lets_talk():
    pyautogui.hotkey('win', 'h')
    
def take_notes():
    # Initialize the speech recognition recognizer
    recognizer = sr.Recognizer()

    speak("Sure, I'm listening. Say 'Stop listening' when you are done.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, phrase_time_limit=5)  # Listen for 5 seconds
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()

            if 'stop listening' in command:
                speak("Stopped taking notes.")
                break

            # Append the recognized command to a file (e.g., notes.txt)
            with open('notes.txt', 'a') as file:
                file.write(command + '\n')
            
            # You can also choose to show the recognized command on the screen
            # print("You said:", command)

        except sr.UnknownValueError:
            # Handle cases where speech recognition couldn't understand the input
            print("Sorry, I couldn't understand what you said.")
        except sr.RequestError:
            # Handle cases where the speech recognition service is unavailable
            print("Sorry, the speech recognition service is currently unavailable.")
        except KeyboardInterrupt:
            # Handle cases where the user interrupts the speech recognition
            print("Stopped taking notes.")
            break
        
def open_notepad():
    # Use the subprocess module to open Notepad
    subprocess.Popen('notepad.exe')
    speak("Opening Notepad.")            
    

def open_website(command):
    # Extract the website name from the command
    website_name = command.lower().replace('open website', '').strip()
    if website_name:
        # Prepare the URL
        if " " in website_name:
            website_name = website_name.replace(" ", "")
        website_url = f'https://{website_name}.com/'
        # Open the website in the default web browser
        webbrowser.open(website_url)
        speak(f"Opening {website_name}.")
    else:
        speak("Please specify the name of the website you want to open.")


def chat_with_openai(prompt):
    print("DEBUG: Initiating OpenAI chat with prompt:", prompt)  # Debugging message
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",  # Choose the language model engine
            prompt=prompt,
            max_tokens=150  # Adjust the max_tokens parameter as needed for the desired response length
        )
        print("DEBUG: OpenAI response:", response)  # Debugging message
        if response.choices and response.choices[0].text:
            return response.choices[0].text.strip()
        else:
            return "No response from OpenAI."
    except Exception as e:
        print("DEBUG: OpenAI API error:", e)  # Debugging message
        return "Error during OpenAI chat."


def main():
    speak("Hello, Mother Fucker, Optimus Prime Reporting for Duty.")
    is_awake = True
    last_command_time = time.time()

    while True:
        command = listen()
        if is_awake:
            if command.lower() == 'sleep':
                speak("Going to sleep. Wake me up by saying 'Optimus Prime'.")
                is_awake = False
            else:
                # Process user commands
                if 'time' in command:
                    # Implement time-related actions
                    pass
                elif 'date' in command:
                    # Implement date-related actions
                    pass
                elif 'Optimus Prime' in command:
                    # Implement actions when the user mentions the assistant's name
                    pass
                elif 'let us talk'in command.lower():
                    lets_talk()
                    speak("Im listening mother fucker")
                    
                elif 'home'in command.lower():
                    home()
                    speak("taking you home motherfucker")
                  

                elif 'table right' in command.lower():
                    tab_right()
                    speak("Tabbed to the right motherfucker.")
                elif 'switch app' in command.lower():
                    switch_app()
                    speak("Transforming App MotherFucker")  
                elif 'word to the left' in command.lower() or 'tab to the left' in command.lower() or 'word to the right' in command.lower():
                    tab_left()
                    speak("Tabbed to the left motherfucker.")
                elif 'loud noises' in command:
                    play_music()
                    speak("loud noises motherfucker")
                elif 'silence' in command:
                    pause_music()
                    speak("no loud noises motherfucker")
                elif 'next song' in command:
                    next_song()
                elif 'play' in command.lower() and 'song' in command.lower():
                    play_song(command)
                elif 'fuck off' in command.lower():
                    close_tab()
                elif 'open website' in command or 'take me to' in command:
                    open_website(command)
                    speak("I will take you to your destination motherfucker")
                elif 'search for' in command.lower():
                    # Extract the search query from the command
                    search_query = command.lower().replace('search for', '').strip()
                    if search_query:
                        # Perform web search using the default web browser
                        webbrowser.open(f"https://www.google.com/search?q={search_query}")
                        speak(f"Here are the top search results for '{search_query}'.")
                    else:
                        speak("Please specify what you want to search for.")
                elif 'chat with me' in command.lower():
                    # Extract the chat prompt from the command
                    chat_prompt = command.lower().replace('chat with me', '').strip()
                    if chat_prompt:
                        # Initiate the chat with the provided prompt
                        response = chat_with_openai(chat_prompt)
                        speak(f"Optimus Prime says: {response}")
                    else:
                        # If no prompt is provided, use the default chat prompt
                        DEFAULT_CHAT_PROMPT = "How are you?"
                        response = chat_with_openai(DEFAULT_CHAT_PROMPT)
                        speak(f"Optimus Prime says: {response}")
                elif 'open notebook' in command.lower() or 'write this down' in command.lower() or 'take a note' in command.lower() or 'let me tell you a story' in command.lower():
                    take_notes()
                    speak("Done taking notes. You can find them in the notebook.")
                elif 'open twitter' in command.lower():
                    open_website('twitter.com')
                    speak("Opening Twitter.")
                elif 'tweet' in command.lower():
                    click_tweet_button()
                    speak("Tweeting the message.")
                # Add code to input the message you want to tweet using pyautogui.typewrite()
                # You can use the listen() function to get the message from your voice input
                # and then use pyautogui.typewrite() to type the message.
                elif 'open notepad' in command.lower():
                    open_notepad()            
                elif 'goodbye motherfuker' in command.lower():
                    speak("Goodbye Mother Fucker! Shutting down.")
                    exit()
                else:
                    # For unrecognized commands, don't speak any response
                    pass
                last_command_time = time.time()

        else:
            if time.time() - last_command_time >= 5:
                speak("Sleeping now.")
                is_awake = True
            else:
                time.sleep(1)  # Wait for 1 second before checking for commands again

if __name__ == "__main__":
    main()
