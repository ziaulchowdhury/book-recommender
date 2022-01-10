# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 00:13:21 2021

@author: ziaul
"""

from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import fuzz
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CollaborativeFilteringRecommender:
    
    def __init__(self, books, ratings):
        
        self.books = books
        self.ratings = ratings
        
        books_col = books[['book_id', 'original_title']]
        books_col = books_col.dropna()
        
        # mapper: dict, map book title name to index of the book in data
        self.mapper = pd.Series(books_col.index, index=books_col['original_title']) 
    
    def train_model(self):
        
        num_users = len(self.ratings.user_id.unique())
        num_items = len(self.ratings.book_id.unique())
        print('There are {} unique users and {} unique movies in this data set'.format(num_users, num_items))
        self.ratings = self.ratings.dropna()
        
        df_ratings_cnt_tmp = pd.DataFrame(self.ratings.groupby('rating').size(), columns=['count'])
        # df_ratings_cnt_tmp.head(10)
        
        total_cnt = num_users * num_items
        rating_zero_cnt = total_cnt - self.ratings.shape[0]

        df_ratings_cnt = df_ratings_cnt_tmp.append(
            pd.DataFrame({'count': rating_zero_cnt}, index=[0.0]),
            verify_integrity=True,
        ).sort_index()
        
        df_ratings_cnt['log_count'] = np.log(df_ratings_cnt['count'])
        # df_ratings_cnt    
        
        # get_ipython().run_line_magic('matplotlib', 'inline')
        ax = df_ratings_cnt[['count']].reset_index().rename(columns={'index': 'rating score'}).plot(
            x='rating score',
            y='count',
            kind='bar',
            figsize=(12, 8),
            title='Count for Each Rating Score (in Log Scale)',
            logy=True,
            fontsize=12,color='black'
        )
        ax.set_xlabel("book rating score")
        ax.set_ylabel("number of ratings")
        plt.show()
        
        df_books_cnt = pd.DataFrame(self.ratings.groupby('book_id').size(), columns=['count'])
        df_books_cnt.head()
        
        # now we need to take only books that have been rated atleast 60 times to get some idea of the reactions of users towards it
        popularity_threshold = 60
        popular_movies = list(set(df_books_cnt.query('count >= @popularity_threshold').index))
        df_ratings_drop = self.ratings[self.ratings.book_id.isin(popular_movies)]
        print('shape of original ratings data: ', self.ratings.shape)
        print('shape of ratings data after dropping unpopular movies: ', df_ratings_drop.shape)
        
        # get number of ratings given by every user
        df_users_cnt = pd.DataFrame(df_ratings_drop.groupby('user_id').size(), columns=['count'])
        df_users_cnt.head()
        
        # Dropping users who have rated less than 50 times
        ratings_threshold = 10 # 50
        active_users = list(set(df_users_cnt.query('count >= @ratings_threshold').index))
        df_ratings_drop_users = df_ratings_drop[df_ratings_drop.user_id.isin(active_users)]
        print('shape of original ratings data: ', self.ratings.shape)
        print('shape of ratings data after dropping both unpopular movies and inactive users: ', df_ratings_drop_users.shape)
        
        book_user_mat = df_ratings_drop_users.pivot(index='book_id', columns='user_id', values='rating').fillna(0)
        self.book_user_mat_sparse = csr_matrix(book_user_mat.values)
        
        # Fitting the model
        self.model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
        self.model_knn.fit(self.book_user_mat_sparse)
    
    def fuzzy_matching(self, fav_book, verbose=True):
        """
        return the closest match via fuzzy ratio. 
        
        Parameters
        ---------
        fav_movie: str, name of user input movie
        Return
        ------
        index of the closest match
        """
        match_tuple = []
        # get match
        for title, idx in self.mapper.items():
            ratio = fuzz.ratio(title.lower(), fav_book.lower())
            if ratio >= 60:
                match_tuple.append((title, idx, ratio))
        # sort
        match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
        if not match_tuple:
            print('Oops! No match is found')
            return
        if verbose:
            print('Found possible matches in our database: {0}\n'.format([x[0] for x in match_tuple]))
        return match_tuple[0][1]
    
    def recommend_books(self, fav_book, n_recommendations=10):
        """
        return top n similar book recommendations based on user's input book
        
        Parameters
        ----------
        model_knn: sklearn model, knn model
        data: book-user matrix
        
        fav_book: str, name of user input book
        n_recommendations: int, top n recommendations
        
        Return
        ------
        list of top n similar book recommendations
        """
        
        # fit
        self.model_knn.fit(self.book_user_mat_sparse)
        idx = self.fuzzy_matching(fav_book, verbose=True)
        if idx is None:
            return [], [] 
        
        print(f'Recommendation system starting to make inference ...... idx >>>  {idx}')
        distances, indices = self.model_knn.kneighbors(self.book_user_mat_sparse[idx], n_neighbors=n_recommendations+1)
        
        raw_recommends = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
        reverse_mapper = {v: k for k, v in self.mapper.items()}
        
        rec = []
        print(f'Recommendations for {fav_book}:')
        for i, (idx, dist) in enumerate(raw_recommends):
            if idx not in reverse_mapper.keys():
                continue
            print(f'{ i+1 }: { reverse_mapper[idx] }, with distance of {dist}')
            rec.append(reverse_mapper[idx])
        
        return rec, indices