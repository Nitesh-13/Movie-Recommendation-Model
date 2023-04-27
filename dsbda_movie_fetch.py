from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import requests


class Movie:
    def __init__(self,df) -> None:
        self.df = df
        self.features = ['keywords', 'cast', 'genres', 'director']

        for feature in self.features:
            self.df[feature] = self.df[feature].fillna('')

    #Returns features of a particular Movie row
    def combFeatures(self,row):
        return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']


    #Returns title from the index of the movie
    def getTitle(self,index):
        return self.df[self.df.index == index]["title"].values[0]


    #Returns cast from the index of the movie
    def getCast(self,index):
        return self.df[self.df.index == index]["cast"].values[0]


    #Returns genre from the index of the movie
    def getGenre(self,index):
        return self.df[self.df.index == index]["genres"].values[0]


    #Returns genre from the index of the movie
    def getDirector(self,index):
        return self.df[self.df.index == index]["director"].values[0]


    #Returns genre from the index of the movie
    def getDate(self,index):
        return self.df[self.df.index == index]["release_date"].values[0]


    #Returns genre from the index of the movie
    def getTagline(self,index):
        return self.df[self.df.index == index]["tagline"].values[0]


    #Returns index from the title of the movie and if not found returns -1
    def getIndex(self,title):
        lowercase_title = title.lower()
        lowercase_df = self.df["title"].str.lower()
        if not lowercase_df.str.contains(lowercase_title).any():
            return -1
        return self.df[lowercase_df == lowercase_title]["index"].values[0]

    #Returns Movies based on genre sorted according to popularity
    def get_movies(self,genre):
        movies = self.df[self.df['genres'].str.contains(genre, case=False)]
        movies = movies.sort_values(by=['popularity'], ascending=False)
        return movies['index']

    # Returns Movies based on cast sorted according to popularity
    def get_movies_cast(self,cast):
        movies = self.df[self.df['cast'].str.contains(cast, case=False)]
        movies = movies.sort_values(by=['popularity'], ascending=False)
        return movies['index']


    def getPostInfo(self,index):
        defaultObj = {'poster_url': 'https://via.placeholder.com/130x207', 'overview': self.getTagline(index)}

        endpoint = 'https://api.themoviedb.org/3/search/movie'
        api_key = '15d2ea6d0dc1d476efbca3eba2b9bbfb'
        params = {'api_key': api_key, 'query': ':'.join(self.getTitle(index).split(':')[:2]).strip()}

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
        return defaultObj
    
    def getSimilarMovies(self,movie_index):

        self.df["combinedFeatures"] = self.df.apply(self.combFeatures,axis=1)
        
        cv = CountVectorizer()
        countMatrix = cv.fit_transform(self.df["combinedFeatures"])
        similarityElement = cosine_similarity(countMatrix)

        similarity_scores = list(enumerate(similarityElement[movie_index]))
        sorted_similar = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:]
        
        return sorted_similar