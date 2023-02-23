'''
> DSBDA Mini Project <

##Topic - Movie Recommendation Model using scikit learn python module

Team Members - 
    - Ajay
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

#Returns index from the title of the movie and if not found returns -1
def getIndex(title):
    if(str((df[df.title == title])).startswith("Empty")):
        return -1
    return df[df.title == title]["index"].values[0]




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
@app.route('/')
def home():
    return render_template('index.html')




#Define the movie recommendation route
@app.route('/', methods=['POST'])
def recommend_movies():
    users_movie = request.form['movie_name']
    movie_index = getIndex(users_movie)

    if movie_index == -1:
        return render_template('index.html', error='Movie not found!')

    movie_ret_count = int(request.form['movie_ret_count'])

    # Fetching Similar Movies From The Dataset and Sorting
    similarity_scores = list(enumerate(similarityElement[movie_index]))
    sorted_similar = sorted(
        similarity_scores, key=lambda x: x[1], reverse=True)[1:]

    # Extract top similar movies
    recommended_movies = []
    i = 0
    for element in sorted_similar:
        recommended_movies.append(getTitle(element[0]))
        i += 1
        if i == movie_ret_count:
            break

    # Render the results template with the recommended movies
    return render_template('index.html', recommended_movies=recommended_movies, movie_name=users_movie,movie_ret_count=movie_ret_count)




if __name__ == '__main__':
    app.run(debug=True)
