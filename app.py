# app.py

import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Initialize Spotify client with OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
    scope="user-read-private"
))

st.title("🎵 Spotify Song Analyzer")
song_name = st.text_input("Enter a song name:")

if song_name:
    st.write(f"Searching for: **{song_name}**")
    try:
        # Search for the song on Spotify
        results = sp.search(q=song_name, type='track', limit=1)
        tracks = results['tracks']['items']

        if not tracks:
            st.warning("No matching track found. Please check your spelling or try another song.")
        else:
            track = tracks[0]
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            track_id = track.get('id')

            # Debug: show track info
            print("Track ID:", track_id)
            st.write(f"Found track: **{track_name}** by **{track_artist}**")
            st.write(f"Spotify ID: `{track_id}`")

            if not track_id:
                st.error("The track does not have a valid Spotify ID.")
            else:
                try:
                    audio_features = sp.audio_features(track_id)[0]
                    if audio_features:
                        st.subheader("🎧 Audio Features")
                        st.json(audio_features)
                    else:
                        st.error("No audio features found for this track.")
                except Exception as e:
                    st.error(f"Failed to fetch audio features: {e}")
                    print(f"Error getting audio features: {e}")

    except Exception as e:
        st.error(f"Something went wrong while searching: {e}")
        print(f"Search error: {e}")
