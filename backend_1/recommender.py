# Data Analysis and Manipulation Tool
import pandas as readData

# Data Visualization for plotting
import seaborn as sns
import matplotlib.pyplot as plt
import cufflinks as cf

# Machine Learning
# Match Similar data based on common words
from sklearn.metrics.pairwise import cosine_similarity

# Converting a Collection words into Token Counts
from sklearn.feature_extraction.text import CountVectorizer

# Rapid Automatic Keyword Extraction
from rake_nltk import Rake

import sys
import json

# Read data from the CSV file to split movies by run time
movieData = readData.read_csv('./data/netflix_titles.csv')

varMovie = movieData.query("type=='Movie'")
varMovie['min'] = varMovie['duration'].str.split(' ', expand=True)[0]
varMovie['min'] = varMovie['min'].astype(int)
varMovie['hr'] = varMovie['min'] / 60

movieRuntime = varMovie.sort_values(by='hr', ascending=False).head(20)
plt.figure(figsize=(10, 7))
sns.barplot(data=movieRuntime, y='title', x='hr', hue='country', dodge=False)
plt.legend(loc='lower right')
plt.title('Top 10 movies by Run Time')
plt.xlabel('Hours')
plt.ylabel('Movie name')
plt.show()

tv = movieData.query("type=='TV Show'")
tv['sea'] = tv['duration'].str.split(' ', expand=True)[0]
tv['sea'] = tv['sea'].astype(int)

top20tv = tv.sort_values(by='sea', ascending=False).head(20)
plt.figure(figsize=(10, 7))
sns.barplot(data=top20tv, y='title', x='sea', hue='country', dodge=False)
plt.legend(loc='lower right')
plt.title('Top TV show by Run Time')
plt.xlabel('Seasons')
plt.ylabel('Movie name')
plt.show()

sns.set(style="darkgrid", palette="pastel", color_codes=True)
plt.figure(figsize=(5, 10))
sns.countplot(y='director', data=movieData, order=movieData['director'].value_counts().head(20).index)
plt.show()

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
indcast = []
ind = movieData.query('country=="India"')
for i in ind['cast']:
    indcast.append(i)
newls = []
for i in indcast:
    newls.append(str(i).split(',')[0])
inddf = readData.DataFrame(newls, columns=['name'])
ind_df = inddf.drop(inddf.query('name=="nan"').index)
print(ind_df)

ind_df['name'].value_counts().head(20).plot(kind="bar", width=1, color='red', edgecolor='lightgreen', figsize=(10, 8))
plt.xlabel("ACTORS")
plt.ylabel("No. Of Movies")
plt.title("Indian stars with max movies on netflix")
plt.show()

us = movieData[movieData['country'].str.contains('United States', na=False)]
uscast = []
for i in us['cast']:
    uscast.append(i)
newls1 = []
for i in uscast:
    newls1.append(str(i).split(',')[0])

usdf = readData.DataFrame(newls1, columns=['name'])
us_df = usdf.drop(usdf.query('name=="nan"').index)
us_df['name'].value_counts().head(20).plot(kind="bar", width=.8, edgecolor='black', figsize=(10, 8))
plt.xlabel("ACTORS")
plt.ylabel("No. Of Movies")
plt.title("US stars with max movies on netflix")
plt.show()

rat = movieData.groupby('rating')[['show_id']].count().reset_index()
plt.figure(figsize=(10, 7))
plt.pie(rat['show_id'], autopct='%1.1f%%', startangle=90, pctdistance=1.2, shadow=True)
centre_circle = plt.Circle((0, 0), 0.4, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.legend(movieData['rating'])
plt.show()

movieData['date'] = readData.to_datetime(movieData['date_added'])
movieData['month'] = movieData['date'].dt.strftime('%b')
movieData.groupby('month')[['rating']].count().reset_index().sort_values(by='rating', ascending=False).plot(kind='bar', \
                                                                                                            width=1,
                                                                                                            color='green',
                                                                                                            figsize=(
                                                                                                            10, 8))
plt.xlabel("Months")
plt.ylabel("Count")
plt.show()

new_df = movieData[['title', 'director', 'cast', 'listed_in', 'description']]
new_df.head()

new_df['director'] = new_df['director'].fillna(' ')
new_df['director'] = new_df['director'].astype('str')

new_df['cast'] = new_df['cast'].fillna(' ')
new_df['cast'] = new_df['cast'].astype('str')

new_df['bag_of_word'] = ''
for index, row in new_df.iterrows():
    plot = row['description']
    r = Rake()
    r.extract_keywords_from_text(plot)
    keyword_score = r.get_word_degrees()
    g = ''.join(row['listed_in'].split(',')).lower()
    d = ''.join(row['director'].replace(' ', '').split(',')).lower()
    a = ' '.join(row['cast'].replace(' ', '').split(',')).lower()
    k = ' '.join(list(keyword_score.keys()))
    row['bag_of_word'] = g + ' ' + ' ' + d + ' ' + a + ' ' + k

mydf = new_df[['title', 'bag_of_word']]
mydf.head()

c = CountVectorizer()
count_mat = c.fit_transform(mydf['bag_of_word'])
cosine_sim = cosine_similarity(count_mat, count_mat)
print(cosine_sim)

indices = readData.Series(mydf['title'])


def recommend_movie(name):
    movie = []
    idx = indices[indices == name].index[0]
    sort_index = readData.Series(cosine_sim[idx]).sort_values(ascending=False)
    top_10 = sort_index.iloc[1:11]
    for i in top_10.index:
        movie.append(indices[i])
    return movie


def readMovieData():
    movieName = sys.stdin.readline()
    return json.loads(movieName)

movieName = readMovieData()


def listToString(movieName):  
    str1 = " "   
    return (str1.join(movieName))   
print(listToString(movieName))

NameofMovie = listToString(movieName)
print(recommend_movie(NameofMovie))
