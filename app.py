import streamlit as st
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

# Safe wrapper to handle rate limiting
def safe_api_call(api_func, *args, **kwargs):
    retry_delay = 10  # seconds
    while True:
        try:
            return api_func(*args, **kwargs)
        except SpotifyException as e:
            if e.http_status == 429:
                st.warning("⚠️ Rate limit reached. Waiting to retry...")
                time.sleep(retry_delay)
            else:
                st.error(f"Spotify error: {e}")
                return None
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return None

# Spotify authentication using Streamlit secrets
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri="https://aeboong-spotify-recommender.streamlit.app",
    scope="user-library-read user-read-private"
))

# Streamlit UI
st.title("🎵 Spotify Song Recommender")

song_name = st.text_input("Enter a song name:")

if song_name:
    st.write(f"🔍 Searching for: **{song_name}**")

    # Search for the song
    results = safe_api_call(sp.search, q=song_name, type='track', limit=1)

    if results is None:
        st.error("Search failed. Try again later.")
    else:
        tracks = results.get('tracks', {}).get('items', [])

        if not tracks:
            st.warning("❌ No matching track found. Try another song.")
        else:
            track = tracks[0]
            track_name = track['name']
            track_artist = track['artists'][0]['name']
            track_id = track.get('id')

            st.success(f"✅ Found: **{track_name}** by **{track_artist}**")
            st.caption(f"Spotify ID: `{track_id}`")

            # Get audio features
            audio_data = safe_api_call(sp.audio_features, [track_id])

            if audio_data and audio_data[0]:
                st.subheader("🎧 Audio Features")
                st.json(audio_data[0])
            else:
                st.warning("⚠️ No audio features available for this track.")

