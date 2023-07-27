import pyttsx3
import speech_recognition as sr
import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import webbrowser
import openai

# Set your OpenAI API key here
openai.api_key = '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'

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
            return "None"

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



def assistant(command, device_id):
    if 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The current time is {current_time}")
    elif 'date' in command:
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        speak(f"Today's date is {current_date}")
    elif 'Optimus Prime' in command:
        speak("Yes, I am here. How can I assist you?")
    elif 'play music' in command:
        # Set your Spotify app credentials
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='c3c967a6332447fcb03dff7886ad6612',
                                                       client_secret='bd7444e194ca4777b3313b61b9e8610c',
                                                       redirect_uri='http://localhost:8000/callback/',
                                                       scope='user-read-playback-state,user-modify-playback-state'))
        
        # Start playback on the first available device
        sp.start_playback(device_id=device_id)
        speak("Playing music on Spotify.")
    elif 'pause music' in command:
        # Set your Spotify app credentials
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='c3c967a6332447fcb03dff7886ad6612',
                                                       client_secret='bd7444e194ca4777b3313b61b9e8610c',
                                                       redirect_uri='http://localhost:8000/callback/',
                                                       scope='user-read-playback-state,user-modify-playback-state'))
        
        # Pause playback on the first available device
        sp.pause_playback()
        speak("Music paused.")
    elif 'next song' in command:
        # Set your Spotify app credentials
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='c3c967a6332447fcb03dff7886ad6612',
                                                       client_secret='bd7444e194ca4777b3313b61b9e8610c',
                                                       redirect_uri='http://localhost:8000/callback/',
                                                       scope='user-read-playback-state,user-modify-playback-state'))
        
        # Skip to the next track on the first available device
        sp.next_track()
        speak("Skipping to the next song.")
    elif 'play' in command.lower() and 'song' in command.lower():
        # Extract the song name from the command
        song_name = command.lower().replace('play', '').replace('song', '').strip()
        if song_name:
            # Set your Spotify app credentials
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='c3c967a6332447fcb03dff7886ad6612',
                                                           client_secret='bd7444e194ca4777b3313b61b9e8610c',
                                                           redirect_uri='http://localhost:8000/callback/',
                                                           scope='user-read-playback-state,user-modify-playback-state'))

            # Search for the song on Spotify
            results = sp.search(q=song_name, type='track', limit=1)
            if results['tracks']['items']:
                # Get the URI of the first track in the search results
                track_uri = results['tracks']['items'][0]['uri']
                # Start playback of the selected track on the first available device
                sp.start_playback(device_id=device_id, uris=[track_uri])
                speak(f"Playing '{results['tracks']['items'][0]['name']}' by {results['tracks']['items'][0]['artists'][0]['name']}.")
            else:
                speak("Sorry, I couldn't find that song on Spotify.")
        else:
            speak("Please specify the name of the song you want to play.")
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
    # Initialize chat_prompt with a default value
        chat_prompt = "How are you?"

    # Extract the chat prompt from the command
        chat_prompt = command.lower().replace('chat with me', '').strip()

    # Initiate the chat with the provided prompt
        response = chat_with_openai(chat_prompt)
        speak(f"Optimus Prime says: {response}")





speak("Hello, I am your personal assistant, Optimus Prime.")
is_awake = True
last_command_time = time.time()
# Get the list of available devices
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='c3c967a6332447fcb03dff7886ad6612',
                                               client_secret='bd7444e194ca4777b3313b61b9e8610c',
                                               redirect_uri='http://localhost:8000/callback/',
                                               scope='user-read-playback-state,user-modify-playback-state'))
devices = sp.devices()
device_id = devices['devices'][0]['id']

while True:
    command = listen()
    if is_awake:
        if command.lower() == 'sleep':
            speak("Going to sleep. Wake me up by saying 'Optimus Prime'.")
            is_awake = False
        else:
            assistant(command, device_id)
            last_command_time = time.time()
    else:
        if time.time() - last_command_time >= 5:
            speak("Sleeping now.")
            is_awake = True
        else:
            time.sleep(1)  # Wait for 1 second before checking for commands
