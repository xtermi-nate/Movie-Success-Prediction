from imdb import IMDb
import numpy as np
from tkinter.scrolledtext import ScrolledText
import tkinter
from tkinter import *
import tkinter as tk
from tkinter import ttk
import io
import base64
from urllib.request import urlopen
import webbrowser
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.backends.backend_tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

year_list = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
genre_list = ['Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Family', 'Fantasy', 'Horror', 'Thriller',
              'Romance', 'Sci-Fi']
ia = IMDb()


# find the ratings of the actor on depending his movie list and depending on year
def find_rating_over_years(movie_list, year_list):
    print("find_rating_over_years")
    m = {}
    y = []
    rating = {}
    for z in movie_list:
        if z.get('year') in year_list:
            movieID = z.getID()
            m = ia.get_movie(movieID)
            if z.get('year') in rating.keys():
                y = rating[z.get('year')]
            else:
                y = []
            if m.get('rating') is not None:
                y.append(m.get('rating'))
                rating[z.get('year')] = y
    return rating


# find the average ratings
def find_average_rating(rating, year_list):
    avg_rating = {}
    for key in year_list:
        if key in rating.keys():
            avg_rating[key] = str(round(np.mean(rating[key]), 2))
        else:
            avg_rating[key] = 0
    return avg_rating


# list of movies of the person (actress and category)
def getMovieList(full_person, category):
    print("inside movie list")
    movies = full_person.get('filmography')
    movie_list = []
    for movie in movies:
        for key in movie.keys():
            if 'actress' in movie.keys():
                movie_list = movie['actress']
            if (key == category):
                movie_list = movie[category]
    return movie_list


# get the genre rating
def getGenreRate(movie_list):
    print("getGenreRate")
    rate = {}
    rating = []
    for movieID in movie_list:
        if movieID.get('year') in year_list:
            mID = movieID.getID()
            details = ia.get_movie(mID)
            if details.get('rating') is not None:
                for genre in details.get('genres'):
                    if genre in rate.keys():
                        rating = rate[genre]
                    else:
                        rating = []
                    rating.append(details.get('rating'))
                    rate[genre] = rating
    return rate


# get average of genre ratings
def getAvgGenre(rate):
    genre_rate = {}
    for key, values in rate.items():
        if (key in genre_list):
            genre_rate[key] = (str(round(np.mean(values), 2)))
    return genre_rate


# get picture, name and url link toimbd of actor
def getURL(full_person):
    photo = full_person.get('full_size headshot')
    name = full_person.get('name')
    URL = ia.get_imdbURL(actor[0])
    return ([photo, name, URL])


# calculate the success rate of an actor
def getSuccessRate(full_person, category):
    print("inside getsucessrate1")
    movie_list = getMovieList(full_person, category)
    rating = find_rating_over_years(movie_list, year_list)
    rate = getGenreRate(movie_list)
    return ([rating, rate])


def getSuccess(full_person, category):
    print("inside get Success rate 1")
    movie_list = getMovieList(full_person, category)
    rate = getGenreRate(movie_list)
    return (rate)


# average rating total & genre
def getAverage(rating, rate):
    avg_rating = find_average_rating(rating, year_list)
    genre_rate = getAvgGenre(rate)
    print(avg_rating)
    print(genre_rate)
    return ([avg_rating, genre_rate])


# get movie list classified by genres
def get_genre_movie_list():
    m2 = ia.get_top250_movies()
    genre_movies_all = {}
    movies_all = []
    for movieID in m2:
        mID = movieID.getID()
        details = ia.get_movie(mID)
        for genre in details.get('genres'):
            if genre in genre_movies_all.keys():
                movies_all = genre_movies_all[genre]
            else:
                movies_all = []
            movies_all.append(movieID)
    genre_movies = {}
    for key in genre_movies_all.keys():
        if (key in genre_list):
            genre_movies[key] = [len(genre_movies_all[key]), 250]
    return genre_movies


# get the cpunt of total movies done, success and genre based success
def getRating(genreList, genre):
    total = 0
    success = 0
    genre_success = 0
    for key, value in genreList.items():
        total = total + len(value)
        for v in value:
            if float(v) >= 7.0:
                success = success + 1
                if key == genre:
                    genre_success = genre_success + 1
    return ([total, success, genre_success])


# main function

def getMoviePrediction(genre, actor1, actor2, director):
    genre_movies = {'Action': [41, 250], 'Adventure': [62, 250], 'Animation': [19, 250], 'Comedy': [45, 250],
                    'Drama': [174, 250], 'Family': [28, 250], 'Fantasy': [30, 250], 'Horror': [6, 250],
                    'Romance': [26, 250], 'Sci-Fi': [30, 250], 'Thriller': [64, 250]}
   # genre_movies = get_genre_movie_list()
    if actor2 == "":
        e2 = 1
        e2o = 1
    else:
        actor2 = ia.search_person(actor2)
        full_person2 = ia.get_person(actor2[0].getID(), info=["filmography"])
        genreA2 = getSuccess(full_person2, 'actor')
        totalA2, successA2, gSuccessA2 = getRating(genreA2, genre)
        gMovieA2 = len(genreA2[genre])
        print(totalA2, successA2, gSuccessA2, gMovieA2)
        if gSuccessA2 == 0 or successA2 == 0 or totalA2 == 0:
            if successA2 == 0:
                e2 = 0.5
            if gSuccessA2 == 0:
                e2o = 0.5
        else:
            e2 = successA2 / totalA2
            e2o = gSuccessA2 / gMovieA2

    actor1 = ia.search_person(actor1)
    full_person1 = ia.get_person(actor1[0].getID(), info=["filmography"])
    genreA1 = getSuccess(full_person1, 'actor')
    totalA1, successA1, gSuccessA1 = getRating(genreA1, genre)
    gMovieA1 = len(genreA1[genre])
    print(totalA1, successA1, gSuccessA1, gMovieA1)
    if gSuccessA1 == 0 or successA1 == 0 or totalA1 == 0:
        if successA1 == 0:
            e1 = 0.5
        if gSuccessA1 == 0:
            e1o = 0.5
    else:
        e1 = successA1 / totalA1
        e1o = gSuccessA1 / gMovieA1

    director = ia.search_person(director)
    full_person3 = ia.get_person(director[0].getID(), info=["filmography"])
    genreD = getSuccess(full_person3, 'director')
    totalD, successD, gSuccessD = getRating(genreD, genre)
    gMovieD = len(genreD[genre])
    print(totalD, successD, gSuccessD, gMovieD)
    if gSuccessD == 0 or successD == 0 or totalD == 0:
        if successD == 0:
            eD = 0.5
        if gSuccessD == 0:
            eDo = 0.5
    else:
        eD = successD / totalD
        eDo = gSuccessD / gMovieD

    Po = (e1o * e2o * eDo) / (e1 * e2 * eD)
    genreS = genre_movies[genre]
    Po = Po * (genreS[0] / genreS[1] * 100)
    if Po > 100:
        Po = 70
    print(e1, e1o, e2, e2o, eD, eDo, Po)
    return Po


# year_list = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,2019]
# genre_list = ['Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Family', 'Fantasy', 'Horror', 'Thriller',
#               'Romance', 'Sci-Fi']
# name = 'keanu Reeves'
# actor = ia.search_person(name)
# full_person = ia.get_person(actor[0].getID(), info=["filmography"])
#
# photo, name, URL = getURL(full_person)
# rating, rate = getSuccessRate(full_person, 'actor')
# avg_rating, genre_rate = getAverage(rating, rate)
# print(rating)
getMoviePrediction("Adventure", "Robert Downey Jr", "Michael Sheen", "Stephen Gaghan")
