# spotify.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from voice import speak

# Set your Spotify app credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='c3c967a6332447fcb03dff7886ad6612',
                                               client_secret='bd7444e194ca4777b3313b61b9e8610c',
                                               redirect_uri='http://localhost:8000/callback/',
                                               scope='user-read-playback-state,user-modify-playback-state'))
devices = sp.devices()
device_id = devices['devices'][0]['id']

def play_music():
    # Start playback on the first available device
    sp.start_playback(device_id=device_id)
    speak("Playing music on Spotify.")
    # Add this code to the 'play_music' function in spotify.py
    devices = sp.devices()
    print("Available devices:", devices)


def pause_music():
    # Pause playback on the first available device
    sp.pause_playback()
    speak("Music paused.")

def next_song():
    # Skip to the next track on the first available device
    sp.next_track()
    speak("Skipping to the next song.")

def play_song(command):
    # Extract the song name from the command
    song_name = command.lower().replace('play', '').replace('song', '').strip()
    if song_name:
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
