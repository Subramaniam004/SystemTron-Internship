import streamlit as st
import pickle
import pandas as pd
import requests 

def featch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index=movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:  
        movie_id=movies.iloc[i[0]].movie_id 
        recommended_movies.append(movies.iloc[i[0]].title)
         #feach poster from API
        recommended_movies_posters.append(featch_poster(movie_id))
    return recommended_movies

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
st.header('Movie Recommender System')
#search box
selected_movie_name= st.selectbox('',movies['title'].values)
if st.button('Recommend'):
    names,posters =recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
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
import streamlit as st
import pickle
import pandas as pd
import requests 
import os

 # Function to fetch movie poster
def featch_poster(movie_id):
     try:
         response = requests.get(
             f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US', 
             timeout=5  # 5-second timeout
         )
         data = response.json()
         return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')
     except requests.exceptions.RequestException:
         return "https://via.placeholder.com/500"  # Placeholder if API fails

 # Function to recommend movies
def recommend(movie):
     movie_index = movies[movies['title'] == movie].index[0]
     distances = similarity[movie_index]
     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

     recommended_movies = []
     recommended_movies_posters = []
    
     for i in movies_list:
         movie_id = movies.iloc[i[0]].movie_id
         recommended_movies.append(movies.iloc[i[0]].title)
         recommended_movies_posters.append(featch_poster(movie_id))  # Append posters too
    
     return recommended_movies, recommended_movies_posters

# # Load files safely
if not os.path.exists('movie_dict.pkl') or not os.path.exists('similarity.pkl'):
     st.error("Required files are missing. Please ensure 'movie_dict.pkl' and 'similarity.pkl' exist.")
else:
     movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
     movies = pd.DataFrame(movies_dict)
     similarity = pickle.load(open('similarity.pkl', 'rb'))

    # Streamlit UI
     st.header('🎬 Movie Recommender System')

     selected_movie_name = st.selectbox("Choose a movie:", movies['title'].values)

     if st.button('Recommend'):
         names, posters = recommend(selected_movie_name)

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
import streamlit as st
import pickle
import pandas as pd
import requests
import os

# # ✅ Replace this with your actual API key from TMDb
API_KEY = "your_new_api_key_here"

# # ✅ Function to Fetch Movie Poster
def fetch_poster(movie_id):
     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    
     try:
         response = requests.get(url, timeout=5)
         data = response.json()

         # ✅ Debugging: Print API response
         print(f"Movie ID: {movie_id} - API Response: {data}")

         # ✅ Check if 'poster_path' exists
         if 'poster_path' in data and data['poster_path']:
             return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
         else:
             print(f"❌ No poster found for Movie ID: {movie_id}")
             return "https://via.placeholder.com/500x750?text=No+Image"

     except requests.exceptions.RequestException as e:
         print(f"❌ API Error: {e}")
         return "https://via.placeholder.com/500x750?text=Error"

# # ✅ Function to Recommend Movies
def recommend(movie):
     try:
         movie_index = movies[movies['title'] == movie].index[0]
         distances = similarity[movie_index]
         movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

         recommended_movies = []
         recommended_movies_posters = []
        
         for i in movies_list:
             movie_id = movies.iloc[i[0]].movie_id
             print(f"Fetching movie poster for ID: {movie_id}")  # Debugging
             recommended_movies.append(movies.iloc[i[0]].title)
             recommended_movies_posters.append(fetch_poster(movie_id))
        
         return recommended_movies, recommended_movies_posters

     except Exception as e:
         print("❌ Recommendation Error:", e)
         return [], []

# # ✅ Load Movie Data
if not os.path.exists('movie_dict.pkl') or not os.path.exists('similarity.pkl'):
     st.error("Required files are missing. Please ensure 'movie_dict.pkl' and 'similarity.pkl' exist.")
else:
     movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
     movies = pd.DataFrame(movies_dict)
     similarity = pickle.load(open('similarity.pkl', 'rb'))

#     # ✅ Streamlit UI
     st.header('🎬 Movie Recommender System')

     selected_movie_name = st.selectbox("Choose a movie:", movies['title'].values)

     if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)

     if not names:
             st.error("No recommendations found. Please try another movie.")
     else:
             cols = st.columns(5)
             for idx, col in enumerate(cols):
                 with col:
                     st.text(names[idx])
                     st.image(posters[idx])





#working code I
import streamlit as st
import pickle
import pandas as pd

# ✅ Function to get Google Image search link
def get_google_image_url(movie_name):
        return f"https://www.google.com/search?tbm=isch&q={movie_name.replace(' ', '+')}+movie+poster"

# ✅ Function to Recommend Movies
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_posters = []
        
        for i in movies_list:
             movie_name = movies.iloc[i[0]].title
             google_image_url = get_google_image_url(movie_name)  # 🔍 Link to Google Images
            
             recommended_movies.append(movie_name)
             recommended_movies_posters.append(google_image_url)
        
        return recommended_movies, recommended_movies_posters

    except Exception as e:
         print("❌ Recommendation Error:", e)
         return [], []

 # ✅ Load Movie Data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

 # ✅ Streamlit UI
st.header('🎬 Movie Recommender System')
st.subheader("Find your next favorite movie! 🍿")

selected_movie_name = st.selectbox("Choose a movie:", movies['title'].values)

if st.button('Recommend'):
    names, google_links = recommend(selected_movie_name)

    if not names:
         st.error("No recommendations found. Please try another movie.")
    else:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
             with col:
                 st.text(names[idx])
                 st.markdown(f"[🔍 View Poster]({google_links[idx]})", unsafe_allow_html=True)