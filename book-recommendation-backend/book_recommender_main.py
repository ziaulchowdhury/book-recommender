# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 21:41:16 2021

@author: ziaul
"""

import pandas as pd
import json

from fastapi import FastAPI
import uvicorn
import nest_asyncio
from fastapi.middleware.cors import CORSMiddleware

from content_based_recommender import ContentBasedRecommender
from data_loader import DataLoader
from desciptive_analysis import DescriptiveAnalysis
from collaborative_filtering_recommender import CollaborativeFilteringRecommender

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    
    # 
    # Data loading and preprocessing
    #
    books_data_loader = DataLoader()
    books, ratings, tags, btags, to_read = books_data_loader.open_datasets()
    ratings, tags, btags, to_r = books_data_loader.clean_datasets()
    books = books_data_loader.create_books_features()
    
    #
    # Visualization 
    #
    '''
    descrip_analysis = DescriptiveAnalysis(books, ratings, tags, btags, to_read, to_r)
    descrip_analysis.visualize_toprated_popular_commonrating()
    descrip_analysis.show_most_popular_genres()
    descrip_analysis.show_edition_vs_rating()
    descrip_analysis.show_treemap_publyear_langcode_avgrating()
    descrip_analysis.show_short_title_vs_long_titles()
    descrip_analysis.show_tags_wordcloud()
    descrip_analysis.show_top_to_read()
    descrip_analysis.show_num_to_read_per_user()
    
    #
    # Recommendation System
    #
    
    #  Content Based Recommendation System
    content_recommender = ContentBasedRecommender(books)
    
    hobbit_recommendation_result = content_recommender.recommend_books('The Hobbit')
    descrip_analysis.show_recommendatation_result_Table(hobbit_recommendation_result)
    
    harry_potter_recommendation_result = content_recommender.recommend_books('Harry Potter and The Chamber of Secrets')
    descrip_analysis.show_recommendatation_result_Table(harry_potter_recommendation_result)
    '''
    # 
    # Collaborative Filtering
    #
    
    colla_filtering_recommender = CollaborativeFilteringRecommender(books, ratings)
    colla_filtering_recommender.train_model()
        
    colla_filtering_recommender.recommend_books(fav_book='To Kill a Mockingbird')
    colla_filtering_recommender.recommend_books(fav_book='Harry Potter and the Chamber of Secrets')
    colla_filtering_recommender.recommend_books(fav_book='Gone Girl')
    colla_filtering_recommender.recommend_books(fav_book='Divergent')
    colla_filtering_recommender.recommend_books(fav_book='Kafka on the Shore')
    
    '''
    @app.get("/content-recommend/")
    async def make_coontent_recommendation(book_title: str = ''):
        return content_recommender.recommend_books(book_title)
    
    @app.get("/colla-recommend/")
    async def make_collaborative_filtering_recommendation_Old(book_title: str = ''):
        return colla_filtering_recommender.recommend_books(book_title)
    '''
    
    @app.get("/book/recommend/collaborative")
    async def make_collaborative_filtering_recommendation(book_id: int):
        book_series = books[books.book_id == book_id]
        book_original_title = book_series['title'].values[0]
        recommended_books, indices = colla_filtering_recommender.recommend_books(book_original_title)
        if len(indices) == 0:
            return pd.DataFrame()
        
        print(f'indices: {indices}')
        recommended_books_series = books.iloc[indices[0]]
        df = pd.DataFrame(recommended_books_series)
        df = df.drop_duplicates(subset=['book_id'], keep=False)
        # df = df.drop(book_series.index)
        return json.loads(df.to_json(orient='table'))
    
    @app.get("/book/search")
    async def search_books(title: str = ''):
        search_result_series = books[books.title.str.contains(title, case=False)].title
        df = pd.DataFrame(search_result_series)
        df['small_image_url'] = books.iloc[df.index]['small_image_url']
        df['image_url'] = books.iloc[df.index]['image_url']
        df['book_id'] = books.iloc[df.index]['book_id']
        return json.loads(df.to_json(orient='table'))
    
    @app.get("/book")
    async def get_book(book_id: int):
        book_series = books[books.book_id == book_id]
        df = pd.DataFrame(book_series)
        return json.loads(df.to_json(orient='table'))
    
    @app.get("/book/recommend/similar_rating")
    async def get_book_by_similar_rating(book_id: int):
        book_series = books[books.book_id == book_id]
        df = books[books['average_rating'] == book_series['average_rating'].values[0]]
           
        if df.shape[0] == 0:
            books_sorted_by_rating = books.sort_values(by=['average_rating'], ascending=False)
            book_iloc_row = books_sorted_by_rating[books_sorted_by_rating.book_id == book_id].iloc[-1]
            book_iloc = books_sorted_by_rating.index.get_loc(book_iloc_row.name)
            if book_iloc > 5 and book_iloc <= books_sorted_by_rating.shape[0]-5:
                df = books_sorted_by_rating.iloc[book_iloc-5: book_iloc+5]
            else:
                df = books_sorted_by_rating.iloc[book_iloc: book_iloc+10]
        
        if df.shape[0] > 10:
            df = df.head(10)
        
        df = df.drop_duplicates(subset=['book_id'], keep=False)
        try:
            df = df.drop(book_series.index)
        except:
            print('Could not find same book!')
        
        return json.loads(df.to_json(orient='table'))
    
    @app.get("/book/recommend/same_author")
    async def get_book_by_same_authors(book_id: int):
        book_series = books[books.book_id == book_id]
        author_name_list = book_series['authors'].values[0].split(',')
        
        dfs = []
        for author_name in author_name_list:
            search_result_series = books[books.authors.str.contains(author_name, case=False)]
            if search_result_series.shape[0] > 0:
                df_tmp = pd.DataFrame(search_result_series)
                dfs.append(df_tmp)
        
        df = pd.concat(dfs)
        if df.shape[0] > 10:
            df = df.head(10)
        
        df = df.drop_duplicates(subset=['book_id'], keep=False)
        try:
            df = df.drop(book_series.index)
        except:
            print('Could not find same book!')
        
        return json.loads(df.to_json(orient='table'))
    
    nest_asyncio.apply()
    uvicorn.run(app, port=8080, host='0.0.0.0')
    
    nest_asyncio.apply()
    uvicorn.run(app, port=8080, host='0.0.0.0')
     