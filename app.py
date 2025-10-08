import streamlit as st
import pandas as pd
import requests
import pickle

# Use st.cache_data to cache the loaded data, so it's only loaded once.
@st.cache_data
def load_data():
    try:
        # Load the two files separately
        with open('movies.pkl', 'rb') as file:
            movies = pickle.load(file)
        with open('cosine_sim.pkl', 'rb') as file:
            cosine_sim = pickle.load(file)
            
        return movies, cosine_sim
    except FileNotFoundError:
        st.error("Error: Data files not found. Please ensure 'movies.pkl' and 'cosine_sim.pkl' are in the same directory.")
        return None, None

# Function to get movie recommendations
def get_recommendations(title, movies_df, cosine_sim):
    try:
        idx = movies_df[movies_df['title'] == title].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]  # Get top 10 similar movies
        movie_indices = [i[0] for i in sim_scores]
        return movies_df.iloc[movie_indices]
    except IndexError:
        st.error("Movie not found in the dataset. Please select a different movie.")
        return pd.DataFrame() # Return an empty DataFrame on error

# --- OMDb API poster fetching ---
def fetch_poster(movie_title):
    omdb_api_key = '9ab3068e'
    if not omdb_api_key:
        st.warning("OMDb API key not set. Posters cannot be displayed.")
        return "https://placehold.co/500x750/cccccc/333333?text=No+Poster"
    
    # We are now using the movie title to search for the movie
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={omdb_api_key}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_url = data.get('Poster')
        if poster_url and poster_url != "N/A":
            return poster_url
        else:
            return "https://placehold.co/500x750/cccccc/333333?text=No+Poster"
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster from OMDb: {e}")
        return "https://placehold.co/500x750/cccccc/333333?text=No+Poster"

# --- Streamlit UI Layout ---
st.set_page_config(
    page_title="Movie Recommendation System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a better look and feel, mimicking IMDb
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #f0f2f6;
    }
    h1 {
        color: #F5C518;
        text-align: center;
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', sans-serif;
    }
    .stSelectbox, .stButton {
        padding: 10px;
        border-radius: 10px;
    }
    .stSelectbox > div > div {
        background-color: #333333;
        color: #f0f2f6;
        border-radius: 5px;
    }
    .stButton > button {
        background-color: #F5C518;
        color: black;
        border: none;
        border-radius: 5px;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button:hover {
        background-color: #d3a40c;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
    .stImage > img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    }
    .movie-title {
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        margin-top: 5px;
        color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")

# Load data only once using the cached function
movies, cosine_sim = load_data()

# Check if data was loaded successfully
if movies is not None and not movies.empty:
    with st.container():
        st.markdown("<h3 style='text-align: center; color: #f0f2f6;'>Select a example movie to get recommendations</h3>", unsafe_allow_html=True)
        selected_movie = st.selectbox("", movies['title'].values, index=0, label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button('Recommend'):
            with st.spinner('Fetching recommendations...'):
                recommendations = get_recommendations(selected_movie, movies, cosine_sim)

    if 'recommendations' in locals() and not recommendations.empty:
        st.markdown("---")
        st.subheader("Top 10 Recommended Movies:")
        st.markdown("<h5 style='text-align: center; color: #f0f2f6;'>Click on the poster to see details</h5>", unsafe_allow_html=True)

        # Create a flexible grid layout for posters
        cols = st.columns(5) # Create 5 columns per row
        
        for i in range(10):
            if i < len(recommendations):
                movie_title = recommendations.iloc[i]['title']
                
                # Pass the movie title to fetch the poster
                poster_url = fetch_poster(movie_title)
                
                with cols[i % 5]: # Use modulo to cycle through columns
                    st.image(poster_url, caption=movie_title, use_container_width=True)
                    st.markdown(f"<p class='movie-title'>{movie_title}</p>", unsafe_allow_html=True)
                    st.markdown("---")
    elif 'recommendations' in locals():
        st.info("No recommendations found for this movie.")