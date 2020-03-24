import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 10]

Data=pd.read_csv("BollywoodActorRanking.csv")
Data_D=pd.read_csv("BollywoodDirectorRanking.csv")
Data_M=pd.read_csv("BollywoodMovieDetail.csv")
Data.head()
Data_M.head(n=603)
Data.describe()
Data_Normalized_Rating=Data.nlargest(10,"normalizedRating")
Data_Normalized_Rating


#rating chart

plt.bar(Data_Normalized_Rating["actorName"],Data_Normalized_Rating["normalizedRating"])
plt.xticks(rotation=45)
plt.show()

Data_highest_films=Data.nlargest(10,"movieCount")
Data_highest_films
Data["movieCount"].sum()
Data_highest_films["movieCount"].sum()

# number of films done
plt.bar(Data_highest_films["actorName"],Data_highest_films["movieCount"])
plt.xticks(rotation=45)
plt.show()


#Google hits actor
Data_highest_google_hits=Data.nlargest(10,"googleHits")
Data_highest_google_hits

plt.bar(Data_highest_google_hits["actorName"],Data_highest_google_hits["googleHits"])
plt.xticks(rotation=45)
plt.show()


#Movie Rank
Data_highest_Movie_Rank=Data.nlargest(10,"normalizedMovieRank")
Data_highest_Movie_Rank
plt.bar(Data_highest_Movie_Rank["actorName"],Data_highest_Movie_Rank["normalizedMovieRank"])
plt.xticks(rotation=45)
plt.show()

#Low Rating
Data_Normalized_Rating=Data.nsmallest(10,"normalizedRating")
Data_Normalized_Rating


#highest movie count director
Data_D_highest_films=Data_D.nlargest(10,"movieCount")
Data_D_highest_films

plt.bar(Data_D_highest_films["directorName"],Data_D_highest_films["movieCount"])
plt.xticks(rotation=45)
plt.show()

Data_M_actors_divide=Data_M[Data_M["actors"].isna()==False]
Data_M_actors_divide.head(n=622)
Data_M_actors_divide.shape

Actors_M=Data_M_actors_divide["actors"]
Actors_M
Actors_M
type(Actors_M)
len(Actors_M)
Actors_M=Actors_M.dropna()
len(Actors_M)
Actors_M=Actors_M.reset_index(drop=True)
len(Actors_M)
x=[]
for i in range(len(Actors_M)):
    #print(Actors_M[i])
    a=Actors_M[i].split("|")
    a=[z.strip() for z in a]
    #print(a)
    #print(i)
    x.append(a)
#print(x)
max_a=0
for i in x:
    #print (len(i))
    if(len(i)>max_a):
        max_a=len(i)
Actors_M1=pd.DataFrame(data=x,columns=["Actor1","Actor2","Actor3","Actor4"])
len(Actors_M1)
Actors_M1

Data_M_actors_divide1=pd.concat([Data_M_actors_divide,Actors_M1],axis=1)
actor1=Data_M_actors_divide1["Actor1"]
actor2=Data_M_actors_divide1["Actor2"]
actor3=Data_M_actors_divide1["Actor3"]
actor4=Data_M_actors_divide1["Actor4"]
actor1=[i for i in actor1]
actor2=[i for i in actor2]
actor3=[i for i in actor3]
actor4=[i for i in actor4]
Actor1=actor1+actor2+actor3+actor4
len(Actor1)
#Actor1.unique()
Actor2=pd.DataFrame(Actor1,columns=["Actor"])
Actor2["Actor"].value_counts()
Actor3=pd.DataFrame(Actor2["Actor"].unique(),columns=["Actor"])
len(Actor3)
Actor3=Actor3.dropna()
Actor3
Actor4=pd.DataFrame(Actor2["Actor"].value_counts())
Actor4.reset_index(level=0,inplace=True)
Actor4

#Ranking of movies by Popular Genre
Data_M_genre_divide=Data_M
Data_M_genre_divide["genre"].unique()
Data_M_genre_divide=Data_M_genre_divide[Data_M_genre_divide["genre"].isna()==False]
Genre_M=Data_M_genre_divide["genre"]
Genre_M=Genre_M.reset_index(drop=True)
Genre_M
G=[]
for i in range(len(Genre_M)):
    #print(Actors_M[i])
    a=Genre_M[i].split("|")
    a=[z.strip() for z in a]
    G.append(a)
max_a=0
for i in G:
    #print (len(i))
    if(len(i)>max_a):
        max_a=len(i)
Genre_M1=pd.DataFrame(data=G,columns=["Genre1","Genre2","Genre3"])
len(Genre_M1)
Genre_M1
Data_M_genre_divide1=pd.concat([Data_M_genre_divide,Genre_M1],axis=1)
genre1=Data_M_genre_divide1["Genre1"]
genre2=Data_M_genre_divide1["Genre2"]
genre3=Data_M_genre_divide1["Genre3"]
genre1=[i for i in genre1]
genre2=[i for i in genre2]
genre3=[i for i in genre3]
Genre1=genre1+genre2+genre3
len(Genre1)
#Actor1.unique()
Genre2=pd.DataFrame(Genre1,columns=["Genre"])
Genre2["Genre"].value_counts()
Genre3=pd.DataFrame(Genre2["Genre"].value_counts())
Genre3
#Graph
plt.rcParams['figure.figsize'] = [15, 10]
Genre3
plt.barh(Genre3.index,Genre3["Genre"])
plt.show()

#Popular Gentre by Year
Data_M_genre_year=Data_M_genre_divide1
Data_M_genre_year1=Data_M_genre_year[["releaseYear","Genre1","Genre2","Genre3"]]
Data_M_genre_year1
Data_M_genre_year2=pd.melt(Data_M_genre_year1,id_vars=["releaseYear"],var_name="Genre_Name",value_name="Genre_Val")
Data_M_genre_year2.drop(["Genre_Name"],axis=1,inplace=True)
Data_M_genre_year2=Data_M_genre_year2.dropna()
Data_M_genre_year2

#plt.bar(Data_M_genre_year2["releaseYear"],Data_M_genre_year2["releaseYear"].value_count())
#plt.show()
Data_M_genre_year3=Data_M_genre_year2.groupby("releaseYear")
Data_M_genre_year3
Data_M_genre_year3
Data_M_genre_year4=pd.DataFrame(columns=Data_M_genre_year2.columns)

for i,j in Data_M_genre_year3:
    Data_M_genre_year4=pd.concat([Data_M_genre_year4,j],ignore_index=True)
Data_M_genre_year4["Genre_Val"].value_counts()
Data_M_genre_year8=Data_M_genre_year4.groupby(["Genre_Val","releaseYear"])
Data_y=pd.DataFrame()
Data_l=[]
for x,y in Data_M_genre_year8:
    Data_l.append({"Genre":x[0],"Year":x[1],"Count":y["Genre_Val"].count()})
Data_y=pd.DataFrame(Data_l)
Data_y=Data_y.set_index("Genre")
Data_y

#plot
for i in (Data_y.index.unique()):
    plt.plot(Data_y[Data_y.index==i].Year,Data_y[Data_y.index==i].Count,label=i)
plt.legend()
#Genre and actor
Data_actor_genre=Data_M_actors_divide1
Data_genre_temp=Data_M_genre_divide1.loc[:,"Genre1":"Genre3"]
Data_genre_temp
Data_actor_genre=pd.concat([Data_M_actors_divide1,Data_genre_temp],axis=1)
Data_actor_genre=Data_actor_genre.loc[:,"Actor1":"Genre3"]
Data_actor_genre