import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"]
))

st.title("🎧 Spotify Song Recommender")

user_input = st.text_input("Enter a song name:")
if user_input:
    results = sp.search(q=user_input, type="track", limit=1)
    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        st.write(f"You selected: {track['name']} by {track['artists'][0]['name']}")

        audio_features = sp.audio_features(track['id'])[0]

        # Load your dataset
        df = pd.read_csv("your_dataset.csv")
        df = df.dropna(subset=["danceability", "energy", "valence", "tempo", "acousticness"])

        # Normalize and compute similarity
        features = ["danceability", "energy", "valence", "tempo", "acousticness"]
        df_scaled = MinMaxScaler().fit_transform(df[features])
        input_vector = MinMaxScaler().fit(df[features]).transform([[
            audio_features["danceability"],
            audio_features["energy"],
            audio_features["valence"],
            audio_features["tempo"],
            audio_features["acousticness"]
        ]])

        df["similarity"] = cosine_similarity(input_vector, df_scaled)[0]
        recommendations = df.sort_values("similarity", ascending=False).head(5)

        st.subheader("Recommended Songs 🎵")
        for i, row in recommendations.iterrows():
            st.write(f"{row['name']} by {row['artists']}")
    else:
        st.warning("Song not found.")

