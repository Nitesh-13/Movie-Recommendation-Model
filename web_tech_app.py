import pandas as pd
import dsbda_movie_fetch
from flask import Flask, request, render_template

# Reading The Dataset
df = pd.read_csv("movie_dataset.csv")

app = Flask(__name__, static_folder='static', template_folder='templates')
movie = dsbda_movie_fetch.Movie(df)


#Define the home page route
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')




#Define the movie recommendation route
@app.route('/movie', methods=['GET'])
def recommend_movies():
    category = request.args.get('category')
    category_value = request.args.get('category_value')
    movie_ret_count = 10
    singlePara = False


    if(category == "Genre Based Movies"):
        fetched_movies = movie.get_movies(category_value)
        singlePara = True
    elif(category == "Actor Based Movies"):
        fetched_movies = movie.get_movies_cast(category_value)
        singlePara = True
    elif(category == "Similar Movies"):
        movie_index = movie.getIndex(category_value)

        if movie_index == -1:
            return render_template('404.html') #404 Page

        fetched_movies = movie.getSimilarMovies(movie_index)



    # Extract top similar movies
    recommended_movies = []

    for element in fetched_movies:
        postandInfo = movie.getPostInfo(element if singlePara else element[0])
        movieObj = {
            "title": movie.getTitle(element if singlePara else element[0]),
            "cast": movie.getCast(element if singlePara else element[0]),
            "genre": movie.getGenre(element if singlePara else element[0]),
            "director": movie.getDirector(element if singlePara else element[0]),
            "release_date": movie.getDate(element if singlePara else element[0]),
            "poster": postandInfo.get('poster_url'),
            "description": postandInfo.get('overview'),
        }
        recommended_movies.append(movieObj)
        if len(recommended_movies) == movie_ret_count:
            break


    # Render the results template with the recommended movies
    return render_template('list.html', recommended_movies=recommended_movies, users_movie=category_value.title(),movie_ret_count=movie_ret_count)




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)