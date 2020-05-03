from __future__ import print_function

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing, tree
from collections import defaultdict
import math

from flask import Flask, request


app = Flask(__name__)


@app.route('/test')
def hello_world():
    return 'Testing connection succeeded'


@app.route('/', methods=['POST'])
def json_example():
    req_data = request.get_json()
    actor1 = req_data['actor1']
    actor2 = req_data['actor2']
    actor3 = req_data['actor3']
    director = req_data['director']
    time = req_data['year']
    budget = req_data['budget']
    faceno = req_data['faceno']
    duration = req_data['duration']
    color = req_data['color']
    c_rating = req_data['c_rating']
    genres = req_data['genre']
    language = req_data['language']
    score = req_data['score']
    aspect_ratio = req_data['aspect_ratio']

    df = pd.read_csv('Stage2Lower.csv', index_col=0)
    tf = pd.read_csv('WithoutGrossLower.csv', index_col=0)
    budget = budget * 1000000

    # director gross and imdb score
    director_entries = df['director_name'] == director
    movies_before_time = df['title_year'] < time

    director_avg_gross = df[director_entries & movies_before_time]['gross'].aggregate(np.mean)

    director_avg_score = df[director_entries & movies_before_time]['imdb_score'].aggregate(np.mean)

    director_movies = df[director_entries & movies_before_time].shape[0]

    # if any column is null or person not found make it zero so it wont affect the calculation
    if math.isnan(director_avg_gross):
        director_avg_gross = 0
    if math.isnan(director_avg_score):
        director_avg_score = 0
    if math.isnan(director_movies):
        director_movies = 0

    # average score/ gross and movies done by actors according to their history in datasets
    def actor_data(actor, time):
        # getting movies before the release year and getting the actor from the 3 actor columns
        actor_movies = df['title_year'] < time
        actor_in_1 = df['actor_1_name'] == actor
        actor_in_2 = df['actor_2_name'] == actor
        actor_in_3 = df['actor_3_name'] == actor

        # score gross and movies if he was in 1st column
        actor_score_1 = df[actor_in_1 & actor_movies]['imdb_score'].aggregate(np.mean)
        actor_gross_1 = df[actor_in_1 & actor_movies]['gross'].aggregate(np.mean)
        actor_movie_1 = df[actor_in_1 & actor_movies].shape[0]
        # score gross and movies if he was in 2st column
        actor_score_2 = df[actor_in_2 & actor_movies]['imdb_score'].aggregate(np.mean)
        actor_gross_2 = df[actor_in_2 & actor_movies]['gross'].aggregate(np.mean)
        actor_movie_2 = df[actor_in_2 & actor_movies].shape[0]
        # score gross and movies if he was in 3rd column
        actor_score_3 = df[actor_in_3 & actor_movies]['imdb_score'].aggregate(np.mean)
        actor_gross_3 = df[actor_in_3 & actor_movies]['gross'].aggregate(np.mean)
        actor_movie_3 = df[actor_in_3 & actor_movies].shape[0]

        # setting values zero if not found so it wont afect calculations
        if math.isnan(actor_score_1):
            actor_score_1 = 0
        if math.isnan(actor_score_2):
            actor_score_2 = 0
        if math.isnan(actor_score_3):
            actor_score_3 = 0
        if math.isnan(actor_gross_1):
            actor_gross_1 = 0
        if math.isnan(actor_gross_2):
            actor_gross_2 = 0
        if math.isnan(actor_gross_3):
            actor_gross_3 = 0
        if math.isnan(actor_movie_1):
            actor_movie_1 = 0
        if math.isnan(actor_movie_2):
            actor_movie_2 = 0
        if math.isnan(actor_movie_3):
            actor_movie_3 = 0

        # getting averages
        actor_avg_score = (actor_score_1 + actor_score_2 + actor_score_3) / 3

        actor_avg_gross = (actor_gross_1 + actor_gross_2 + actor_gross_3) / 3

        actor_movie = (actor_movie_1 + actor_movie_2 + actor_movie_3)
        # setting zero to avoid error in calcuation and make it unaffecting
        if math.isnan(actor_avg_score):
            actor_avg_score = 0
        if math.isnan(actor_avg_gross):
            actor_avg_gross = 0
        if math.isnan(actor_movie):
            actor_movie = 0

        return actor_avg_score, actor_avg_gross, actor_movie

    actor_1_avg_score, actor_1_avg_gross, actor_1_movies = actor_data(actor1, time)
    actor_2_avg_score, actor_2_avg_gross, actor_2_movies = actor_data(actor2, time)
    actor_3_avg_score, actor_3_avg_gross, actor_3_movies = actor_data(actor3, time)

    average_score_actors = (actor_1_avg_score + actor_2_avg_score + actor_3_avg_score) / 3
    average_gross_actors = (actor_1_avg_gross + actor_2_avg_gross + actor_3_avg_gross) / 3
    total_movies = (actor_1_movies + actor_2_movies + actor_3_movies)

    # appending the new data to train and predict
    sd = tf.copy()

    sd = sd.append(
        {'color': color, 'duration': duration, 'genres': genres, 'facenumber_in_poster': faceno, 'language': language,
         'content_rating': c_rating, 'budget': budget, 'title_year': time, 'imdb_score': score,
         'aspect_ratio': aspect_ratio, 'director_avg_gross': director_avg_gross, 'director_movies': director_movies,
         'director_avg_score': director_avg_score, 'actor_average_score': average_score_actors,
         'actor_average_gross': average_gross_actors, 'actor_movies': total_movies}, ignore_index=True)

    genre = sd['genres']
    genre_num = pd.DataFrame()
    del sd['genres']
    # splitting the genres and count of it
    count = 0
    for i in genre:
        s = i.split('|')
        for j in s:
            genre_num.at[count, j] = 1
            count = count + 1

    le = defaultdict(preprocessing.LabelEncoder)
    genre_num = genre_num.fillna('0')
    encode_list = sd.select_dtypes(include=['object']).copy()

    encode_data = pd.DataFrame()
    encode_data = pd.get_dummies(encode_list)

    # remove currently unaffecting columns (add them later)
    del sd['language']
    del sd['color']
    del sd['content_rating']
    sd = sd.join(encode_data)
    sd = sd.reset_index(drop=True)
    sd = sd.join(genre_num)
    print("Encoding data is done")
    print("Using the model and predicting.....")

    # applying random forest regression
    pres = pd.DataFrame()
    pres = pres.append(sd[len(sd) - 1:], ignore_index=True)
    sd = sd.drop(sd.index[len(sd) - 1])
    b = sd.gross_class
    a = sd.drop('gross_class', axis=1)
    a.isna().sum()
    pres = pres.drop('gross_class', axis=1)
    # calling the algorithm
    algo = RandomForestRegressor(n_estimators=1000, max_depth=10)
    algo = algo.fit(a, b)
    out = algo.predict(pres)

    # the classes of gross calculations
    gross_rate = out[0]
    gross = ""
    # minimum = 0
    # maximum = 0
    if gross_rate <= 1:
        minimum = 0
        maximum = 1
        gross = "Upto 1 Million Dollars"

    if 1 < gross_rate <= 2:
        minimum = 1
        maximum = 10
        gross = "1 to 10 Million Dollars"
    if 2 < gross_rate <= 3:
        minimum = 10
        maximum = 20
        gross = "10 to 20 Million Dollars"
    if 3 < gross_rate <= 4:
        minimum = 20
        maximum = 40
        gross = "20 to 40 Million Dollars"
    if 4 < gross_rate <= 5:
        minimum = 40
        maximum = 65
        gross = "40 to 65 Million Dollars"
    if 5 < gross_rate <= 6:
        minimum = 65
        maximum = 100
        gross = "65 to 100  Million Dollars"
    if 6 < gross_rate <= 7:
        minimum = 100
        maximum = 150
        gross = "100 to 150 Million Dollars"
    if 7 < gross_rate <= 8:
        minimum = 150
        maximum = 200
        gross = "150 to 200 Million Dollars"
    if 8 < gross_rate <= 9:
        minimum = 200
        maximum = 300
        gross = "200+ Million Dollars"
    print("The predicted approximate gross revenue of the movie is:")
    print(gross)
    avg = np.mean(maximum + minimum)
    print(avg)

    if (((maximum + minimum) / 2) * 1000000) >= (budget + (budget / 2)):
        success = "The movie is a success"
    else:
        success = "The movie is not a success"
    return '''
               The predicted approximate gross revenue of the movie is: {}
               The movie is: {}'''.format(gross, success)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
