#Andrew Holzwarth, Tom Murray, Brett Carey

# Questions bot will answer (allowing for different phrasing):
# 1: What were the top 10 movies in 2020?
    # [Best Movies Netflix]
# 2: How long was the highest ranked movie in 2015?
    # [Best Movies Netflix]
# 3: How many shows have a ranking above 7.5?
    # [Best Shows Netflix]
# 4: What were the top 10 shows on Netflix in 2018?
    # [Best Shows Netflix]
# 5: What was the genre of the best movie in 2016?
    # [Best Movies Netflix]
# 6: In 2008, what was the lowest ranked movie?
    # [Best Movies Netflix, Best Shows Netflix]
# 7: What is the runtime of the longest Netflix movie released in 2013
    # [raw_titles]
# 8: What show had the most seasons on Netflix?
    # [raw_titles]
# 9: What genre was the top Netflix show in 2019?
    # [Best Shows Netflix]
# 10: How many movies released in 2009 were rated "R"
    # [raw_titles]


import pandas as pd
import pymongo

'''
Part 1
'''
# Read in the data
best_movies = pd.read_csv(r'Best Movies Netflix.csv')
best_shows = pd.read_csv(r'Best Shows Netflix.csv')
raw_titles = pd.read_csv(r'raw_titles.csv')

# Drop columns that contain unused data
best_movies = best_movies[['TITLE',	'RELEASE_YEAR',	'SCORE', 'DURATION', 'MAIN_GENRE']]
best_shows = best_shows[['TITLE',	'RELEASE_YEAR',	'SCORE', 'MAIN_GENRE']]
raw_titles = raw_titles[['type', 'release_year', 'age_certification',	'runtime', 'seasons']]

'''
Part 2
'''
#Connect to Mongo
host_name = "localhost"
port = "27017"

conn_str = {"local" : f"mongodb://{host_name}:{port}/",}
client = pymongo.MongoClient(conn_str["local"])

#Create Database
db_name = "Final_Project"
db = client[db_name]

#Create Collections
collection1_name = "Best_Movies"
collection1 = db[collection1_name]

collection2_name = "Best_Shows"
collection2 = db[collection2_name]

collection3_name = "Raw_Titles"
collection3 = db[collection3_name]

# Best Movies into Mongo
best_movies.reset_index(inplace=True)
best_movies_dict = best_movies.to_dict('records')
collection1.insert_many(best_movies_dict)

# Best Shows into Mongo
best_shows.reset_index(inplace=True)
best_shows_dict = best_shows.to_dict('records')
collection2.insert_many(best_shows_dict)

# Raw Titles into Mongo
raw_titles.reset_index(inplace=True)
raw_titles_dict = raw_titles.to_dict('records')
collection3.insert_many(raw_titles_dict)
