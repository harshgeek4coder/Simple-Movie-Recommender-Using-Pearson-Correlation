# -*- coding: utf-8 -*-
"""Simple Movie Recommender System.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/harshgeek4coder/Simple-Movie-Recommender-Using-Pearson-Correlation/blob/master/Simple%20Movie%20Recommender%20System.ipynb

# Simple Movie Recommender System :

we will focus on providing a basic recommendation system by suggesting items that are most similar to a particular item, in this case, movies. Keep in mind, this is not a true robust recommendation system, to describe it more accurately,it just tells you what movies/items are most similar to your movie choice.
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

column_names=['user_id','item_id','rating','timestamp']
df_data=pd.read_csv('u.data',names=column_names,sep='\t')

df_data.head()

"""Now we will try to get movie titles :"""

movie_df=pd.read_csv('Movie_Id_Titles')
movie_df.head()

df=pd.merge(df_data,movie_df)

df.head()

df.info()

df.describe().T

df.isnull().sum()

"""## EDA :

### Movies with their respective Average Ratings :
"""

df.groupby('title')['rating'].mean().sort_values(ascending=False)

"""### Top Movies Liked By The User :"""

df.groupby('title')['rating'].count().sort_values(ascending=False).head(10)

ratings=pd.DataFrame(df.groupby('title')['rating'].mean())
ratings.head()

ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())
ratings.head()

sns.set_style('darkgrid')
plt.figure(figsize=(12,4))
ratings['num of ratings'].hist(bins=30)
plt.xlabel('Number Of Ratings')

ratings['rating'].hist()
plt.xlabel('Ratings')

sns.jointplot(x='rating',y='num of ratings',data=ratings)

"""## Building Simple Recommendation System :

Now let's create a matrix that has the user ids on one access and the movie title on another axis. Each cell will then consist of the rating the user gave to that movie. Note there will be a lot of NaN values, because most people have not seen most of the movies.
"""

moviemat=df.pivot_table(index='user_id',columns='title',values='rating')

moviemat.head()

"""#### Most Rated Top 10 Movies :"""

ratings.sort_values('num of ratings',ascending=False).head(10)

"""SO now , Let Us Choose Two Movies Of Two Different Genres:
    
    Sci-Fi :Star Wars
    
    Comedy :Liar Liar

##### Let us grab ratings of these two movies :
"""

starwars_rating=moviemat['Star Wars (1977)']
starwars_rating.head()

liarliar_rating=moviemat['Liar Liar (1997)']
liarliar_rating.head()

"""### Now, We can then use corrwith() method to get correlations between two pandas series:"""

similar_to_starwars=moviemat.corrwith(starwars_rating)

similar_to_liarliar=moviemat.corrwith(liarliar_rating)

"""### Creating Coorelation Table : """

corr_starwars=pd.DataFrame(similar_to_starwars,columns=['Coorelation'])

corr_starwars.dropna(inplace=True)
#Dropping Null Values Ratings

corr_starwars.head()

corr_starwars.sort_values('Coorelation',ascending=False).head(10)

"""#### Now if we sort the dataframe by correlation, we should get the most similar movies, however note that we get some results that don't really make sense. This is because there are a lot of movies only watched once by users who also watched star wars (it was the most popular movie).

#### Let's fix this by filtering out movies that have less than 100 reviews (this value was chosen based off the histogram from earlier).
"""

corr_starwars=corr_starwars.join(ratings['num of ratings'])

corr_starwars.head()

print("Recommendations Based on Similarity :")
print('\n')
corr_starwars[corr_starwars['num of ratings']>100].sort_values('Coorelation',ascending=False).head(10)

"""## Now the same for the comedy Liar Liar:"""

corr_liarliar = pd.DataFrame(similar_to_liarliar,columns=['Correlation'])
corr_liarliar.dropna(inplace=True)
corr_liarliar = corr_liarliar.join(ratings['num of ratings'])
print("Recommendations Based on Similarity :")
print('\n')
corr_liarliar[corr_liarliar['num of ratings']>100].sort_values('Correlation',ascending=False).head(10)

