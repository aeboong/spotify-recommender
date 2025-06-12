import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler

# Load CSV directly from GitHub
@st.cache_data
def load_data():
    csv_url = "https://github.com/aeboong/spotify-recommender/raw/main/SpotifyFeatures.csv"
    df = pd.read_csv(csv_url)
    return df

df = load_data()

# Streamlit UI
st.title("🎵 Song Recommender")

song_options = df['track_name'].unique()
selected_song = st.selectbox("Select a song you like:", song_options)

# Recommendation logic
if selected_song:
    # Features to use
    features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness']

    # Filter dataset to match the selected song
    song_data = df[df['track_name'] == selected_song].iloc[0]

    # Normalize features
    scaler = StandardScaler()
    feature_data = scaler.fit_transform(df[features])
    selected_song_features = scaler.transform([song_data[features]])

    # Compute similarity
    similarity = cosine_similarity(selected_song_features, feature_data)[0]

    # Get top recommendations
    df['similarity'] = similarity
    recommendations = df[df['track_name'] != selected_song].sort_values(by='similarity', ascending=False).head(5)

    st.subheader("🔁 Recommended Songs")
    for _, row in recommendations.iterrows():
        st.write(f"**{row['track_name']}** by *{row['artist_name']}*")


