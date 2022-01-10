# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 00:05:03 2021

@author: ziaul
"""

import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
import seaborn as sns
import plotly.express as px
import plotly.io as pio
import pandas as pd
import plotly.graph_objects as go
from wordcloud import WordCloud
from collections import Counter

class DescriptiveAnalysis:
    
    def __init__(self, books, ratings, tags, btags, to_read, to_r):
        
        self.books = books
        self.ratings = ratings
        self.tags = tags
        self.btags = tags
        self.to_read = to_read
        self.to_r = to_r
        
    def visualize_data(self, books_to_display):
        
        for i in range(0, 9):
            fig = plt.figure(figsize=(10, 10))
            response = requests.get(books_to_display['image_url'].iloc[i])
            img = Image.open(BytesIO(response.content))
            ax = fig.add_subplot(1, 2, 1, xticks=[], yticks=[])
            ax.imshow(img)
            
            ax = fig.add_subplot(1, 2, 2)
            plt.axis('off')
            ax.plot()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.text(0, 0.5, books_to_display['title'].iloc[i], fontsize=20, wrap=True)
            plt.show()
            
    def visualize_toprated_popular_commonrating(self):
        
        # Top rated books
        print('Visualizing top rated books .....')
        top_rated_books = self.books.sort_values('average_rating', ascending=False)
        self.visualize_data(top_rated_books.head(10))
        
        # Most popular books
        print('Visualizing most popular books .....')
        most_popular_books = self.books.sort_values(by='ratings_count', ascending=False)
        self.visualize_data(most_popular_books.head(10))
        
        # Most Common Rating Values
        plt.figure(figsize=(16,8))
        sns.distplot(a=self.books['average_rating'], kde=True, color='r')
        plt.show()
        
        no_of_ratings_per_book = self.ratings.groupby('book_id').count()
        plt.figure(figsize=(16,8))
        sns.distplot(a=no_of_ratings_per_book['rating'], color='g')
        plt.show()
        
        # Highly rated authors
        top_authors = top_rated_books[['authors', 'average_rating']]
        top_authors = top_authors.head(20)
        # top_authors.plot.barh(x='authors', y='average_rating')
        pio.renderers.default = 'browser'
        fig = px.bar(top_authors, x='authors', y='average_rating', color ='average_rating')
        fig.show()
        
    def show_most_popular_genres(self):
        
        # Finding popular genres and books available for those.
        joint_tags = pd.merge(self.tags, self.btags, left_on='tag_id', right_on='tag_id', how='inner')
        p = joint_tags.groupby('tag_name').count()
        p = p.sort_values(by='count', ascending=False)
        genres=["Art", "Biography", "Business", "Chick Lit", "Children's", "Christian", "Classics", "Comics", "Contemporary", "Cookbooks", "Crime", "Ebooks", "Fantasy", "Fiction", "Gay and Lesbian", "Graphic Novels", "Historical Fiction", "History", "Horror", "Humor and Comedy", "Manga", "Memoir", "Music", "Mystery", "Nonfiction", "Paranormal", "Philosophy", "Poetry", "Psychology", "Religion", "Romance", "Science", "Science Fiction", "Self Help", "Suspense", "Spirituality", "Sports", "Thriller", "Travel", "Young Adult"]
        for i in range(len(genres)):
            genres[i] = genres[i].lower()
        self.new_tags = p[p.index.isin(genres)]
        pio.renderers.default = 'browser'
        fig = go.Figure(go.Bar(x=self.new_tags['count'], y=self.new_tags.index, orientation='h'))
        fig.show()
        
    def show_edition_vs_rating(self):
        
        # Analysing the relation between no of editions and ratings
        pio.renderers.default = 'browser'
        fig = px.line(self.books, y="books_count", x="average_rating", title='Book Count VS Average Rating')
        fig.show()
        
    def show_treemap_publyear_langcode_avgrating(self):
        
        dropna = self.books.dropna()
        pio.renderers.default = 'browser'
        fig = px.treemap(dropna, path=['original_publication_year', 'language_code', "average_rating"], color='average_rating')
        fig.show()
        
    def show_short_title_vs_long_titles(self):
         
        # Do readers prefer short titles or long titles?
        self.books['length-title'] = self.books['original_title'].str.len()
        plt.figure(figsize=(16,8))
        sns.regplot(x=self.books['length-title'], y=self.books['average_rating'])
        
    def show_tags_wordcloud(self):
        
        # Word Cloud for tags used by readers
        text = self.new_tags.index.values
        wordcloud = WordCloud().generate(str(text))
        plt.figure(figsize = (8, 8), facecolor = None)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
    
    def show_top_to_read(self):
        
        to_r20 = self.to_r.head(20)
        pio.renderers.default = 'browser'
        fig = px.bar(to_r20, x=to_r20.index, y='book_id', color ='book_id')
        fig.show()
        
    def show_num_to_read_per_user(self):
        
        # Analysis of number of books in "to read" category of a user.
        to_read1 = self.to_read.groupby('user_id').count()
        c = Counter(list(to_read1['book_id']))
        pio.renderers.default = 'browser'
        fig = go.Figure(data=[go.Scatter(x=list(c.keys()), y=list(c.values()), mode='markers')])
        fig.show()
        
    def show_recommendatation_result_Table(self, recommendation_results):
        
        pio.renderers.default = 'browser'
        fig = go.Figure(data=[go.Table(header=dict(values=recommendation_results, fill_color='orange'))])
        fig.show()
        
        