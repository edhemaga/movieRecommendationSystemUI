from flask.helpers import url_for
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def get_title(index, df):
    return df[df.index == index]["title"].values[0]


def get_index(title, df):
    try:
        return df[df.title == title]["index"].values[0]
    except:
        print("Movie couldn't be found")


def feature_combiner(row):
    try:
        return row["keywords"] + " " + row["cast"] + " " + row["genres"] + " " + row["director"] + " " + row["director"]
    except:
        print("Error: ", row)


def import_data():
    return pd.read_csv('src/data/dataset.csv')


def get_recommended_movie(title):

    # Importing data from the dataset (CSV)
    df = import_data()

    # Selecting features
    features = ["keywords", "cast", "genres", "director"]

    # Handle null values
    for feature in features:
        df[feature] = df[feature].fillna("")

    # Feature combiner
    df["feature_combiner"] = df.apply(feature_combiner, axis=1)

    # Count matrix
    cv = CountVectorizer()
    matrix = cv.fit_transform(df["feature_combiner"])

    # Cosine similarity
    cs = cosine_similarity(matrix)

    # Movie user input and corresponding index

    movie_index = get_index(title, df)

    # Find movies that are similar
    similar_movies = list(enumerate(cs[movie_index]))

    # Sort movies in reverse order in order to firstly display movies with highest similarity
    sorted_list = sorted(similar_movies, key=lambda x: x[1], reverse=True)

    # Output title of movies, set counter to display first n movies
    cnt = 0
    return_list = []
    for item in sorted_list:
        if cnt != 0:
            if cnt < 11:
                return_list.append(get_title(item[0], df))
            else:
                break
        cnt += 1
    return return_list

get_recommended_movie("Avatar")