import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="🎶 CSV-Based Song Recommender")

st.title("🎧 Local Song Recommender (CSV-based)")
st.markdown("Get recommendations based on **audio features** like danceability, energy, valence, tempo, and acousticness.")

# File uploader
uploaded_file = st.file_uploader("Upload your Spotify CSV file (with audio features)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Check if required columns exist
    required_cols = ['name', 'artists', 'danceability', 'energy', 'valence', 'tempo', 'acousticness']
    if all(col in df.columns for col in required_cols):

        # Normalize feature columns
        features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness']
        scaler = MinMaxScaler()
        scaled_features = scaler.fit_transform(df[features])

        # Compute cosine similarity matrix
        similarity_matrix = cosine_similarity(scaled_features)

        # Song selector
        song_list = df['name'].unique()
        selected_song = st.selectbox("🎵 Choose a song from your dataset:", song_list)

        if selected_song:
            n = st.slider("How many recommendations?", min_value=1, max_value=10, value=3)

            # Recommendation logic
            song_idx = df[df['name'] == selected_song].index[0]
            similarity_scores = list(enumerate(similarity_matrix[song_idx]))
            ranked = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

            # Filter top similar but not too similar
            recommendations = []
            for i, score in ranked:
                if i != song_idx and score < 0.95:  # Avoid exact or nearly exact matches
                    recommendations.append(i)
                if len(recommendations) == n:
                    break

            st.subheader("🔁 Recommended Songs")
            st.dataframe(df.iloc[recommendations][['name', 'artists']].reset_index(drop=True))

    else:
        st.error(f"Your CSV must contain these columns: {', '.join(required_cols)}")
else:
    st.info("👈 Please upload a CSV file to begin.")
