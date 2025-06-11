import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# Spotify Credentials
client_id = st.secrets["SPOTIFY_CLIENT_ID"]
client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🎵 Spotify Song Recommender")

song_input = st.text_input("Enter a song name:")

if song_input:
    results = sp.search(q=song_input, type="track", limit=1)
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        track = tracks[0]
        song_id = track['id']
        st.success(f"Found: {track['name']} by {track['artists'][0]['name']}")
        
        # Get audio features
        features = sp.audio_features([song_id])[0]
        st.write("Audio Features:", features)
    else:
        st.error("No song found.")
