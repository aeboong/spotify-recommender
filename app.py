import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify authentication using Streamlit secrets
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri="https://aeboong-spotify-recommender.streamlit.app",
    scope="user-library-read user-read-private"
))

st.title("🎵 Spotify Song Recommender")
song_name = st.text_input("Enter a song name:")

if song_name:
    st.write(f"Searching for: **{song_name}**")
    try:
        results = sp.search(q=song_name, type='track', limit=1)
        tracks = results['tracks']['items']

        if not tracks:
            st.warning("No matching track found. Please check your spelling or try another song.")
        else:
            track = tracks[0]
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            track_id = track.get('id')

            st.write(f"Found track: **{track_name}** by **{track_artist}**")
            st.write(f"Spotify ID: `{track_id}`")

            # ✅ Here's where you paste the audio features code:
            try:
                features_response = sp.audio_features([track_id])
                audio_features = features_response[0]

                if audio_features:
                    st.subheader("🎧 Audio Features")
                    st.json(audio_features)
                else:
                    st.warning("No audio features found for this track.")
            except spotipy.exceptions.SpotifyException as e:
                st.error(f"Failed to fetch audio features: {e}")
                print(f"SpotifyException: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
                print(f"General error: {e}")

    except Exception as e:
        st.error(f"Something went wrong during search: {e}")
        print(f"Search error: {e}")
