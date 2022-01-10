# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 00:26:08 2021

@author: ziaul
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class DataLoader:
    
    def __init__(self):
        print('DataLoader .....')
        
    def open_datasets(self):
        
        self.books = pd.read_csv('./../dataset/goodbooks-10k/books.csv', error_bad_lines=False)
        self.ratings = pd.read_csv('./../dataset/goodbooks-10k/ratings.csv')
        self.tags = pd.read_csv('./../dataset/goodbooks-10k/book_tags.csv')
        self.btags = pd.read_csv('./../dataset/goodbooks-10k/tags.csv')
        self.to_read = pd.read_csv("./../dataset/goodbooks-10k/to_read.csv")
        
        return self.books, self.ratings, self.tags,  self.btags, self.to_read

    def clean_datasets(self):
        
        self.ratings = self.ratings.sort_values("user_id")
        self.ratings.drop_duplicates(subset=["user_id", "book_id"], keep=False, inplace=True)
        
        self.btags.drop_duplicates(subset='tag_id', keep=False, inplace=True)
        
        self.tags.drop_duplicates(subset=['tag_id', 'goodreads_book_id'], keep=False, inplace=True)
        
        to_r = self.books.merge(self.to_read, left_on='book_id', right_on='book_id', how='inner')
        to_r = to_r.groupby('original_title').count()
        self.to_r = to_r.sort_values(by='book_id', ascending=False)
        
        return self.ratings, self.tags, self.btags, self.to_r
    
    def create_books_features(self):
        
        scaler = MinMaxScaler()
        self.books['ratings_count_scaled'] = scaler.fit_transform(self.books[['ratings_count']])
        self.books['ratings_credebility'] = self.books['ratings_count_scaled'] * self.books['average_rating']
        self.books['ratings_credebility'] = scaler.fit_transform(self.books[['ratings_credebility']])
        
        return self.books
        