import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    try:
        # API call to fetch movie details
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US')
        data = response.json()
        if 'poster_path' in data and data['poster_path']:
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        st.error(f"")
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

def recommend(movie_name):
    try:
        # Find the index of the selected movie
        movie_index = movies[movies['title'] == movie_name].index[0]
        distances = similarity[movie_index]
        # Get the top 5 recommended movies
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        for i in movie_list:
            movie_id = movies.iloc[i[0]].movie_id

            recommended_movies.append(movies.iloc[i[0]].title)
            # Fetch poster from API
            recommended_movies_posters.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("Movie not found. Please try another title.")
        return [], []
    except Exception as e:
        st.error(f"")
        return [], []

# Load movie data
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

# Load similarity data
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("Movie Recommender")

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values)

if st.button('Recommend movie'):
    names, posters = recommend(selected_movie_name)

    if names:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])
    else:
        st.error("No recommendations available. Please try again.")
