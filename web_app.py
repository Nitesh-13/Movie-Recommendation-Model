'''
> DSBDA Mini Project <

##Topic - Movie Recommendation Model using scikit learn python module

Team Members - 
    - Vivek
    - Prajakta
    - Shivani
    - Prasad
    - Nitesh

Categories : Holly/Bolly - Genre - Actors - Series
'''




#Importing ML Modules
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import requests
from flask import Flask, request, render_template




# Reading The Dataset
df = pd.read_csv("movie_dataset.csv")
features = ['keywords', 'cast', 'genres', 'director']




#Returns features of a particular Movie row
def combFeatures(row):
    return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']


#Returns title from the index of the movie
def getTitle(index):
    return df[df.index == index]["title"].values[0]


#Returns cast from the index of the movie
def getCast(index):
    return df[df.index == index]["cast"].values[0]


#Returns genre from the index of the movie
def getGenre(index):
    return df[df.index == index]["genres"].values[0]


#Returns genre from the index of the movie
def getDirector(index):
    return df[df.index == index]["director"].values[0]


#Returns genre from the index of the movie
def getDate(index):
    return df[df.index == index]["release_date"].values[0]


#Returns genre from the index of the movie
def getTagline(index):
    return df[df.index == index]["tagline"].values[0]


#Returns index from the title of the movie and if not found returns -1
def getIndex(title):
    lowercase_title = title.lower()
    lowercase_df = df["title"].str.lower()
    if not lowercase_df.str.contains(lowercase_title).any():
        return -1
    return df[lowercase_df == lowercase_title]["index"].values[0]

#Returns Movies based on genre sorted according to popularity
def get_movies(genre):
    movies = df[df['genres'].str.contains(genre, case=False)]
    movies = movies.sort_values(by=['popularity'], ascending=False)
    return movies['index']

# Returns Movies based on cast sorted according to popularity
def get_movies_cast(cast):
    movies = df[df['cast'].str.contains(cast, case=False)]
    movies = movies.sort_values(by=['popularity'], ascending=False)
    return movies['index']




#Returns movie poster url from the title of the movie and not found returns placeholder
def getPostInfo(index):
    defaultObj = {'poster_url': 'https://via.placeholder.com/130x207', 'overview': getTagline(index)}

    endpoint = 'https://api.themoviedb.org/3/search/movie'
    api_key = '15d2ea6d0dc1d476efbca3eba2b9bbfb'
    params = {'api_key': api_key, 'query': ':'.join(getTitle(index).split(':')[:2]).strip()}

    response = requests.get(endpoint, params=params)
    data = response.json()
    results = data.get('results', [])
    if results:
        first_result = results[0]
        poster_path = first_result.get('poster_path')
        if poster_path:
            poster_url = f'https://image.tmdb.org/t/p/original{poster_path}'
        else:
            poster_path = 'https://via.placeholder.com/130x207'
        overview = first_result.get('overview')
        overview = overview.split('.')[0].strip() + '.'
        return {'poster_url': poster_url, 'overview': overview}

    # If no poster URL is found, return placeholder
    return defaultObj




#Removing Null/Empty Values from the data set and creating single feature column
for feature in features:
    df[feature] = df[feature].fillna('')
df["combinedFeatures"] = df.apply(combFeatures,axis=1)




#Plotting similarity using count matrix
cv = CountVectorizer()
countMatrix = cv.fit_transform(df["combinedFeatures"])
similarityElement = cosine_similarity(countMatrix)




#Initializing Flask Application
app = Flask(__name__, static_folder='static', template_folder='templates')


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
        fetched_movies = get_movies(category_value)
        singlePara = True
    elif(category == "Actor Based Movies"):
        fetched_movies = get_movies_cast(category_value)
        singlePara = True
    elif(category == "Similar Movies"):
        movie_index = getIndex(category_value)

        if movie_index == -1:
            return render_template('404.html') #404 Page

        # Fetching Similar Movies From The Dataset and Sorting
        similarity_scores = list(enumerate(similarityElement[movie_index]))
        fetched_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:]



    # Extract top similar movies
    recommended_movies = []

    for element in fetched_movies:
        postandInfo = getPostInfo(element if singlePara else element[0])
        movieObj = {
            "title": getTitle(element if singlePara else element[0]),
            "cast": getCast(element if singlePara else element[0]),
            "genre": getGenre(element if singlePara else element[0]),
            "director": getDirector(element if singlePara else element[0]),
            "release_date": getDate(element if singlePara else element[0]),
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