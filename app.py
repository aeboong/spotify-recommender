import streamlit as st
import pandas as pd
import zipfile
import io
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="Spotify Song Recommender", layout="centered")
st.title("🎧 Spotify Song Recommender")

# Step 1: Load dataset from zipped CSV on GitHub
@st.cache_data
def load_data_from_zip():
    zip_url = "https://github.com/aeboong/spotify-recommender/raw/main/spotifyfeatures.csv.zip"
    response = requests.get(zip_url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        with z.open("SpotifyFeatures.csv") as f:
            return pd.read_csv(f)

df = load_data_from_zip()

# Step 2: Show song picker
song_options = df['track_name'] + " - " + df['artist_name']
selected_song = st.selectbox("Choose a song you like:", song_options)

# Step 3: Recommend similar songs
if selected_song:
    # Find the index of the selected song
    track, artist = selected_song.split(" - ")
    song_row = df[(df['track_name'] == track) & (df['artist_name'] == artist)]

    if song_row.empty:
        st.error("Song not found in dataset.")
    else:
        st.success(f"Generating recommendations for: **{track}** by **{artist}**")

        # Select audio features for similarity
        features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness']
        X = df[features]

        # Normalize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Compute cosine similarity
        similarity = cosine_similarity(X_scaled)

        # Get recommendations
        idx = song_row.index[0]
        similar_indices = similarity[idx].argsort()[::-1][1:6]  # Top 5 (skip self)

        st.subheader("🎯 Recommended Songs:")
        for i in similar_indices:
            rec_track = df.iloc[i]['track_name']
            rec_artist = df.iloc[i]['artist_name']
            st.write(f"- **{rec_track}** by **{rec_artist}**")

