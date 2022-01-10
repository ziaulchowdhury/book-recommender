# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 00:05:34 2021

@author: ziaul
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBasedRecommender:
    
    def __init__(self, books):
        
        self.books = books
        
        self.fillnabooks = self.books.fillna('')
        
        def clean_data(x):
            return str.lower(x.replace(" ", ""))
        
        features = ['original_title', 'authors', 'average_rating']
        self.fillednabooks = self.fillnabooks[features]
        fillednabooks = self.fillednabooks.astype(str)
        for feature in features:
            self.fillednabooks[feature] = self.fillednabooks[feature].apply(clean_data)
        
        def create_soup(x):
            return x['original_title']+ ' ' + x['authors'] + ' ' + x['average_rating']
        
        fillednabooks['soup'] = fillednabooks.apply(create_soup, axis=1) 

        self.count = CountVectorizer(stop_words='english')
        self.count_matrix = self.count.fit_transform(self.fillednabooks['soup'])
        self.cosine_sim = cosine_similarity(self.count_matrix, self.count_matrix)
        
        self.fillednabooks = self.fillednabooks.reset_index()
        self.indices = pd.Series(self.fillednabooks.index, index=fillednabooks['original_title'])
    
    def recommend_books(self, title, result_count=10):
        
        title = title.replace(' ','').lower()
        idx = self.indices[title]
    
        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(self.cosine_sim[idx]))
    
        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1 : result_count+1]
    
        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]
    
        # Return the top 10 most similar movies
        return list(self.books['original_title'].iloc[movie_indices])
    