# Questions bot will answer (allowing for different phrasing):
# 1: What were the top X movies in year Y 
    # [Best Movies Netflix]
# 2: How long was the highest ranked movie in year X 
    # [Best Movies Netflix]
# 3: How many shows have a ranking above X 
    # [Best Shows Netflix]
# 4: What were the top X shows on Netflix in year Y 
    # [Best Shows Netflix]
# 5: What was the most common genre among the best movie rankings in year Y 
    # [Best Movies Netflix]
# 6: In year X, did the top movie or the top show have a higher ranking
    # [Best Movies Netflix, Best Shows Netflix]
# 7: What is the average runtime of Netflix movies released in year X
    # [raw_titles]
# 8: What is the average number of seasons for shows released in year X
    # [raw_titles]
# 9: What genre was the top Netflix show in year X
    # [Best Shows Netflix]
# 10: How many movies released in year X were rated "R"
    # [raw_titles]

import pandas as pd

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

