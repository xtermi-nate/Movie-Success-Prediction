from __future__ import print_function

#import graphviz
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing, tree
from collections import defaultdict
import math

df = pd.read_csv('Stage2Lower.csv', index_col=0)
tf = pd.read_csv('WithoutGrossLower.csv', index_col=0)
print("******************Welcome to Movie Success Predictor*******************")

actor1 = input('Enter Actor 1 Name: ')
actor2 = input('Enter Actor 2 Name: ')
actor3 = input('Enter Actor 3 Name: ')
director = input('Enter Director Name: ')
time = int(input('Enter movie year: '))
budget = int(input('Enter movie budget in million US dollars: '))
budget = budget * 1000000
faceno = int(input('Enter face number in poster: '))
duration = int(input('Enter duration of movie in minutes: '))
color = input('Enter color of movie(Color/Black and White): ')
c_rating = input('Enter content rating(PG-13/PG/G/R/Approved/X/Not Rated/M/Unrated/Passed/NC-17): ')
genres = input('Enter genre of movie(Seperate genres with \'|\' between different genres): ')
language = input('Enter language of movie: ')
score = float(input('Enter imdb score: '))
aspect_ratio = float(input('Enter Aspect Ratio: '))
actor1 = actor1.lower()
actor2 = actor2.lower()
actor3 = actor3.lower()
director = director.lower()
color = color.lower()
c_rating = c_rating.lower()
genres = genres.lower()
language = language.lower()

# Director Average gross, score and total movies
a = df['director_name'] == director
b = df['title_year'] < time

c = df[a & b]['gross'].aggregate(np.mean)
d = df[a & b]['imdb_score'].aggregate(np.mean)
e = df[a & b].shape[0]
if math.isnan(c):
    c = 0
if math.isnan(d):
    d = 0
if math.isnan(e):
    e = 0
director_avg_gross = c
director_avg_score = d
director_movies = e

# Average IMDB score of actors according to their previous movies
a = df['actor_1_name'] == actor1
b = df['actor_2_name'] == actor1
c = df['actor_3_name'] == actor1
d = df['title_year'] < time
x = df[a & d]['imdb_score'].aggregate(np.mean)
y = df[b & d]['imdb_score'].aggregate(np.mean)
z = df[c & d]['imdb_score'].aggregate(np.mean)
if math.isnan(x):
    x = 0
if math.isnan(y):
    y = 0
if math.isnan(z):
    z = 0
e = (x + y + z) / 3
if math.isnan(e):
    e = 0

a = df['actor_1_name'] == actor2
b = df['actor_2_name'] == actor2
c = df['actor_3_name'] == actor2
x = df[a & d]['imdb_score'].aggregate(np.mean)
y = df[b & d]['imdb_score'].aggregate(np.mean)
z = df[c & d]['imdb_score'].aggregate(np.mean)
if math.isnan(x):
    x = 0
if math.isnan(y):
    y = 0
if math.isnan(z):
    z = 0
f = (x + y + z) / 3
if math.isnan(f):
    f = 0

a = df['actor_1_name'] == actor3
b = df['actor_2_name'] == actor3
c = df['actor_3_name'] == actor3
x = df[a & d]['imdb_score'].aggregate(np.mean)
y = df[b & d]['imdb_score'].aggregate(np.mean)
z = df[c & d]['imdb_score'].aggregate(np.mean)
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
actor_avg_score = h

# Average gross of actors according to their previous movies
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
actor_avg_gross = h

# Total movies of actors according to their previous movies
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
actor_movies = h

print("Encoding Data....")
ft = tf.copy()
ft = ft.append(
    {'color': color, 'duration': duration, 'genres': genres, 'facenumber_in_poster': faceno, 'language': language,
     'content_rating': c_rating, 'budget': budget, 'title_year': time, 'imdb_score': score,
     'aspect_ratio': aspect_ratio, 'director_avg_gross': director_avg_gross, 'director_movies': director_movies,
     'director_avg_score': director_avg_score, 'actor_average_score': actor_avg_score,
     'actor_average_gross': actor_avg_gross, 'actor_movies': actor_movies}, ignore_index=True)
le = defaultdict(preprocessing.LabelEncoder)
s = ft['genres']
del ft['genres']
genre_num = pd.DataFrame()
k = 0
for i in s:
    l = i.split('|')

    for j in l:
        genre_num.at[k, j] = 1
    k = k + 1
genre_num = genre_num.fillna('0')
x_list_encode = ft.select_dtypes(include=['object']).copy()
endcode_data = pd.DataFrame()
endcode_data = pd.get_dummies(x_list_encode)
del ft['color']
del ft['language']
del ft['content_rating']
ft = ft.join(endcode_data)
ft = ft.reset_index(drop=True)
ft = ft.join(genre_num)
print("Data Encoding Complete")
print("Applying Algorithm and predicting results.....")

Pre = pd.DataFrame()
Pre = Pre.append(ft[len(ft) - 1:], ignore_index=True)
ft = ft.drop(ft.index[len(ft) - 1])
y = ft.gross_class
X = ft.drop('gross_class', axis=1)
X.isna().sum()
Pre = Pre.drop('gross_class', axis=1)
clf_rf = RandomForestRegressor(n_estimators=1000, max_depth=10)
clf_rf = clf_rf.fit(X, y)
y_1 = clf_rf.predict(Pre)


#clf_rf = tree.DecisionTreeClassifier()
#tree.plot_tree(clf_rf.fit(X, y))

#dot_data = tree.export_graphviz(clf_rf, out_file=None)
# dot_data = tree.export_graphviz(clf_rf, out_file=None,feature_names=X,class_names=y,filled=True, rounded=True,special_characters=True)
#graph = graphviz.Source(dot_data)
#graph.render("Movie Success Prediction")

GROSS_CLASS = y_1[0]
gross = ""
if GROSS_CLASS <= 1:
    gross = "Upto 1 Million Dollars"
if GROSS_CLASS > 1 and GROSS_CLASS <= 2:
    gross = "1 to 10 Million Dollars"
if GROSS_CLASS > 2 and GROSS_CLASS <= 3:
    gross = "10 to 20 Million Dollars"
if GROSS_CLASS > 3 and GROSS_CLASS <= 4:
    gross = "20 to 40 Million Dollars"
if GROSS_CLASS > 4 and GROSS_CLASS <= 5:
    gross = "40 to 65 Million Dollars"
if GROSS_CLASS > 5 and GROSS_CLASS <= 6:
    gross = "65 to 100  Million Dollars"
if GROSS_CLASS > 6 and GROSS_CLASS <= 7:
    gross = "100 to 150 Million Dollars"
if GROSS_CLASS > 7 and GROSS_CLASS <= 8:
    gross = "150 to 200 Million Dollars"
if GROSS_CLASS > 8 and GROSS_CLASS <= 9:
    gross = "200+ Million Dollars"
print("The predicted approximate gross revenue of the movie is:")
print(gross)
