from __future__ import print_function
import pandas as pd
import numpy as np
import math

import matplotlib.pyplot as plt
import os
import seaborn as sns
import sklearn
from sklearn import preprocessing
from collections import  defaultdict
from sklearn import linear_model, pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score


df = pd.read_csv('movie_metadata.csv')

#remove unnecessary columns
del df['director_facebook_likes']
del df['num_critic_for_reviews']
del df['actor_1_facebook_likes']
del df['actor_2_facebook_likes']
del df['actor_3_facebook_likes']
del df['num_user_for_reviews']
del df['num_voted_users']
del df['movie_facebook_likes']
del df['movie_imdb_link']
del df['cast_total_facebook_likes']
del df['plot_keywords']

#the required columns
clean_data= df[df['director_name'].notnull() & df['facenumber_in_poster'].notnull()& df['color'].notnull() & df['duration'].notnull() & df['actor_2_name'].notnull() & df['genres'].notnull()
               & df['actor_1_name'].notnull() & df['actor_3_name'].notnull() & df['country'].notnull()
               & df['title_year'].notnull() & df['budget'].notnull() & df['gross'].notnull() & df['aspect_ratio'].notnull() & df['language'].notnull() & df['content_rating'].notnull()]
df=clean_data
# selecting country wise prediction to usa as the movies are made there
# its difficult to find global rate with so many variables which may arise
usa=df['country']=='USA'
df=df[usa]

df = df.dropna(how='any' ,axis=0)

df['director_avg_gross']=0.0
df['director_avg_score']=0.0
df['director_movies']=0

#calculate and populate above columns

for index,row in df.iterrows():
    director=row['director_name']
    time = row['title_year']
    a=df['director_name']==director
    b=df['title_year']<time

    c=df[a & b]['gross'].aggregate(np.mean)
    d = df[a & b]['imdb_score'].aggregate(np.mean)
    e = df[a & b].shape[0]

    if math.isnan(c):
        c=0
    if math.isnan(d):
        d=0
    if math.isnan(e):
        e=0
    df.at[index, 'director_avg_gross']=c
    df.at[index, 'director_avg_score'] = d
    df.at[index, 'director_movies'] = e

#cleaning actor data (for actor 1 2 and 3)

#average imdb score for actors
df['actor_average_score'] = 0.0
for index, row in df.iterrows():
    actor1 = row['actor_1_name']
    time = row['title_year']
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
    actor2 = row['actor_2_name']
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
    actor3 = row['actor_3_name']
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
    df.at[index, 'actor_average_score'] = h

#average gross for actors

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


#movies done by actors

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



#writting new csv with newly populated + necessary data

df.to_csv('Stage2Final.csv')


#read the created data for further data to add
df=pd.read_csv('Stage2Final.csv',index_col=0)
#print(df.isna().sum())  #check delete later


# create the gross classes and populate column

df['gross_class']=1
for index,row in df.iterrows():
    gross=row['gross']
    gross_class=1
    if gross>=1000000.0 and gross<10000000.0:
            gross_class=2
    if gross>=10000000.0 and gross<20000000.0:
            gross_class=3
    if gross>=20000000.0 and gross<40000000.0:
            gross_class=4
    if gross>=40000000.0 and gross<65000000.0:
            gross_class=5
    if gross>=65000000.0 and gross<100000000.0:
            gross_class=6
    if gross>=100000000.0 and gross<150000000.0:
            gross_class=7
    if gross>=150000000.0 and gross<200000000.0:
            gross_class=8
    if gross>=200000000.0:
            gross_class=9
    df.at[index,'gross_class']=gross_class

del df['country']
del df['director_name']
del df['movie_title']
del df['actor_1_name']
del df['actor_2_name']
del df['actor_3_name']

# creaqte csv with onlygross and other variables
df.to_csv('WithGrossFinal.csv')

#create a csv without gross and only variables

del df['gross']

df.to_csv('WithoutGrossFinal.csv')
#print("done")

# import the new csv and proceed with data training

#df=pd.read_csv('WithoutGrossFinal.csv',index_col=0)
#fd=pd.read_csv('Stage2Final.csv',index_col=0)

#print(df.isna().sum())

fd = pd.read_csv('WithoutGrossFinal.csv' ,index_col=0)

#split genres and add

s=fd['genres']
genre_num=pd.DataFrame()
k=0
for i in s:
    l=i.split('|')

    for j in l:
        genre_num.at[k,j]=1
    k=k+1

genre_num=genre_num.fillna('0')
del fd['genres']
fd=fd.reset_index(drop=True)

x_list_encode = fd.select_dtypes(include=['object']).copy()

encode_data=pd.get_dummies(x_list_encode)

fd=fd.join(encode_data)
fd=fd.join(genre_num)

del fd['color']
del fd['language']
del fd['content_rating']

y=fd.gross_class
X=fd.drop('gross_class',axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

n_folds=5
#set random state to ensure we get samesplits every time
kf = KFold(n_splits=n_folds)
kf = kf.get_n_splits(X_train)

print('training randomforest')

clf_rf = RandomForestRegressor(n_estimators=1000,max_depth=10)
clf_rf = clf_rf.fit(X_train,y_train)
classifier_score = clf_rf.score(X_test,y_test)
print('the classifier accuracy scoreis {:.2f}'.format(classifier_score))

#average of 3 fold cross-validation
score = cross_val_score(clf_rf,X_test,y_test,cv=kf)
print ('The {}-fold cross-validation accuracy score for this classifier is {:.2f}'.format(n_folds, score.mean()))

x_1=X_test['budget']
y_1=clf_rf.predict(X_test)

plt.figure()
plt.scatter(x_1,y_test,c="darkorange",label="data")
plt.scatter(x_1,y_1,color="cornflowerblue", label="max_depth=5")
plt.xlabel("data")
plt.ylabel("target")
plt.title("Random Forest Regression")
plt.legend
plt.show()


