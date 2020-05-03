from __future__ import print_function
import pandas as pd
import numpy as np
import math

df = pd.read_csv('movie_metadata.csv')

# remove unnecessary columns

df = df.drop(
    ['director_facebook_likes', 'plot_keywords', 'cast_total_facebook_likes', 'movie_imdb_link', 'movie_facebook_likes',
     'num_voted_users', 'num_user_for_reviews', 'actor_3_facebook_likes', 'actor_2_facebook_likes',
     'num_critic_for_reviews', 'actor_1_facebook_likes'], axis=1)

# the required columns

clean_data = df[df['actor_1_name'].notnull()
                & df['actor_2_name'].notnull()
                & df['actor_3_name'].notnull()
                & df['duration'].notnull()
                & df['director_name'].notnull()
                & df['genres'].notnull()
                & df['facenumber_in_poster'].notnull()
                & df['content_rating'].notnull()
                & df['language'].notnull()
                & df['gross'].notnull()
                & df['budget'].notnull()
                & df['title_year'].notnull()
                & df['aspect_ratio'].notnull()
                & df['country'].notnull()
                & df['color'].notnull()]
df = clean_data

# selecting country wise prediction to usa as the movies are made there
# its difficult to find global rate with so many variables which may arise
usa = df['country'] == 'USA'
df = df[usa]

df = df.dropna(how='any', axis=0)

# calculate for directors
df['director_movies'] = 0
df['director_avg_score'] = 0.0
df['director_avg_gross'] = 0.0

for index, row in df.iterrows():
    time = row['title_year']
    director = row['director_name']

    d_name = df['director_name'] == director
    year = df['title_year'] < time

    d_gross = df[d_name & year]['gross'].aggregate(np.mean)
    d_score = df[d_name & year]['imdb_score'].aggregate(np.mean)
    d_movies = df[d_name & year].shape[0]

    if math.isnan(d_gross):
        d_gross = 0
    if math.isnan(d_score):
        d_score = 0
    if math.isnan(d_movies):
        d_movies = 0
    df.at[index, 'director_avg_gross'] = d_gross
    df.at[index, 'director_avg_score'] = d_score
    df.at[index, 'director_movies'] = d_movies

# cleaning actor data (for actor 1 2 and 3)

# average imdb score for actors
df['actor_average_score'] = 0.0

for index, row in df.iterrows():
    time = row['title_year']
    actor1 = row['actor_1_name']

    years = df['title_year'] < time

    act_1 = df['actor_1_name'] == actor1
    act_2 = df['actor_2_name'] == actor1
    act_3 = df['actor_3_name'] == actor1
    score_1 = df[act_1 & years]['imdb_score'].aggregate(np.mean)
    if math.isnan(score_1):
        score_2 = 0
    score_2 = df[act_2 & years]['imdb_score'].aggregate(np.mean)
    if math.isnan(score_2):
        score_2 = 0
    score_3 = df[act_3 & years]['imdb_score'].aggregate(np.mean)
    if math.isnan(score_3):
        score_3 = 0
    act_1_score = (score_1 + score_2 + score_3) / 3
    if math.isnan(act_1_score):
        act_1_score = 0

    actor2 = row['actor_2_name']
    act_4 = df['actor_1_name'] == actor2
    act_5= df['actor_2_name'] == actor2
    act_6 = df['actor_3_name'] == actor2
    score1 = df[act_4 & years]['imdb_score'].aggregate(np.mean)
    if math.isnan(score1):
        score1 = 0
    score2 = df[act_5 & years]['imdb_score'].aggregate(np.mean)
    if math.isnan(score2):
        score2 =0
    score3 = df[act_6 & years]['imdb_score'].aggregate(np.mean)
    if math.isnan(score3):
        score3 =0
    act_2_score = (score1 + score2 + score3) / 3
    if math.isnan(act_2_score):
        act_2_score = 0

    actor3 = row['actor_3_name']
    act_7 = df['actor_1_name'] == actor3
    act_8 = df['actor_2_name'] == actor3
    act_9 = df['actor_3_name'] == actor3
    score4 = df[act_7 & years]['imdb_score'].aggregate(np.mean)
    if math.isnan(score4):
        score4 =0
    score5 = df[act_8 & years]['imdb_score'].aggregate(np.mean)
    if math.isnan(score5):
        score5 = 0
    score6 = df[act_9 & years]['imdb_score'].aggregate(np.mean)
    if math.isnan(score6):
        score6 = 0
    act_3_score = (score4 + score5 + score6) / 3
    if math.isnan(act_3_score):
        act_3_score = 0
    act_avg_score = (act_1_score + act_2_score + act_3_score)/3

    if math.isnan(act_avg_score):
        act_avg_score = 0
    df.at[index, 'actor_average_score'] = act_avg_score

# average gross for actors

df['actor_average_gross'] = 0.0
for index, row in df.iterrows():
    actor1 = row['actor_1_name']
    time = row['title_year']
    a = df['actor_1_name'] == actor1
    b = df['actor_2_name'] == actor1
    c = df['actor_3_name'] == actor1
    d = df['title_year'] < time
    x = df[a & d]['gross'].aggregate(np.mean)
    y = df[b & d]['gross'].aggregate(np.mean)
    z = df[c & d]['gross'].aggregate(np.mean)
    if math.isnan(x):
        x = 0
    if math.isnan(y):
        y = 0
    if math.isnan(z):
        z = 0
    e = (x + y + z) / 3
    if math.isnan(e):
        e = 0
    actor2 = row['actor_2_name']
    a = df['actor_1_name'] == actor2
    b = df['actor_2_name'] == actor2
    c = df['actor_3_name'] == actor2
    x = df[a & d]['gross'].aggregate(np.mean)
    y = df[b & d]['gross'].aggregate(np.mean)
    z = df[c & d]['gross'].aggregate(np.mean)
    if math.isnan(x):
        x = 0
    if math.isnan(y):
        y = 0
    if math.isnan(z):
        z = 0
    f = (x + y + z) / 3
    if math.isnan(f):
        f = 0
    actor3 = row['actor_3_name']
    a = df['actor_1_name'] == actor3
    b = df['actor_2_name'] == actor3
    c = df['actor_3_name'] == actor3
    x = df[a & d]['gross'].aggregate(np.mean)
    y = df[b & d]['gross'].aggregate(np.mean)
    z = df[c & d]['gross'].aggregate(np.mean)
    if math.isnan(x):
        x = 0
    if math.isnan(y):
        y = 0
    if math.isnan(z):
        z = 0
    g = (x + y + z) / 3
    if math.isnan(g):
        g = 0
    h = (e + f + g) / 3

    if math.isnan(h):
        h = 0
    df.at[index, 'actor_average_gross'] = h

# movies done by actors

df['actor_movies'] = 0
for index, row in df.iterrows():
    actor1 = row['actor_1_name']
    time = row['title_year']
    a = df['actor_1_name'] == actor1
    b = df['actor_2_name'] == actor1
    c = df['actor_3_name'] == actor1
    d = df['title_year'] < time
    x = df[a & d].shape[0]
    y = df[b & d].shape[0]
    z = df[c & d].shape[0]
    if math.isnan(x):
        x = 0
    if math.isnan(y):
        y = 0
    if math.isnan(z):
        z = 0
    e = x + y + z
    if math.isnan(e):
        e = 0
    actor2 = row['actor_2_name']
    a = df['actor_1_name'] == actor2
    b = df['actor_2_name'] == actor2
    c = df['actor_3_name'] == actor2
    x = df[a & d].shape[0]
    y = df[b & d].shape[0]
    z = df[c & d].shape[0]
    if math.isnan(x):
        x = 0
    if math.isnan(y):
        y = 0
    if math.isnan(z):
        z = 0
    f = x + y + z
    if math.isnan(f):
        f = 0
    actor3 = row['actor_3_name']
    a = df['actor_1_name'] == actor3
    b = df['actor_2_name'] == actor3
    c = df['actor_3_name'] == actor3
    x = df[a & d].shape[0]
    y = df[b & d].shape[0]
    z = df[c & d].shape[0]
    if math.isnan(x):
        x = 0
    if math.isnan(y):
        y = 0
    if math.isnan(z):
        z = 0
    g = x + y + z
    if math.isnan(g):
        g = 0
    h = (e + f + g)

    if math.isnan(h):
        h = 0
    df.at[index, 'actor_movies'] = h

# writting new csv with newly populated + necessary data

df.to_csv('Stage2Final.csv')

# read the created data for further data to add
df = pd.read_csv('Stage2Final.csv', index_col=0)
# print(df.isna().sum())  #check delete later


# create the gross classes and populate column

df['gross_class'] = 1
for index, row in df.iterrows():
    gross = row['gross']
    gross_class = 1
    if 1000000.0 <= gross < 10000000.0:
        gross_class = 2
    if 10000000.0 <= gross < 20000000.0:
        gross_class = 3
    if 20000000.0 <= gross < 40000000.0:
        gross_class = 4
    if 40000000.0 <= gross < 65000000.0:
        gross_class = 5
    if 65000000.0 <= gross < 100000000.0:
        gross_class = 6
    if 100000000.0 <= gross < 150000000.0:
        gross_class = 7
    if 150000000.0 <= gross < 200000000.0:
        gross_class = 8
    if gross >= 200000000.0:
        gross_class = 9
    df.at[index, 'gross_class'] = gross_class

del df['country']
del df['director_name']
del df['movie_title']
del df['actor_1_name']
del df['actor_2_name']
del df['actor_3_name']

# create csv with onlygross and other variables
df.to_csv('WithGrossFinal.csv')

# create a csv without gross and only variables

del df['gross']

df.to_csv('WithoutGrossFinal.csv')
