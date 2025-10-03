from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import requests 

app = Flask(__name__)

# --- Helper function to fetch movie posters ---
def fetch_poster(movie_id):
    
    api_key = "c335b6f4b2e0bba2e8134efea387e88d" 
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Poster"
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750.png?text=Error"


# --- Load the saved files from your notebook ---
movie_dict = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))


# --- Define the routes ---
@app.route('/')
def home():
    return render_template('index.html')

# New route to provide movie titles for autocomplete
@app.route('/movies')
def get_movie_titles():
    titles = movies['title'].tolist()
    return jsonify(titles)


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json(force=True)
    movie_title = data['movie']
    
    try:
        # Get recommendations using your similarity matrix
        movie_index = movies[movies['title'] == movie_title].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        # Prepare the response with titles and posters
        recommendations = []
        for i in movies_list:
            # We use the 'movie_id' from your data to fetch the poster
            movie_id = movies.iloc[i[0]].movie_id
            recommendations.append({
                'title': movies.iloc[i[0]].title,
                'poster_url': fetch_poster(movie_id)
            })
        
        return jsonify({'recommendations': recommendations})

    except IndexError:
        return jsonify({'error': 'Movie not found in the dataset.'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)