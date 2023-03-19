import nltk
from nltk.corpus import stopwords
import os
import re
import pandas as pd
from datetime import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

# basic settings
default_df = pd.read_csv('test/imdb_top250_metadata.csv', header=0)
default_rw = pd.read_csv('test/High and Low_reviews.csv', header=0)


# print(default_df.review_number.sort_values(ascending=True).head(10))


# helper functions
def movie_duration_to_minutes(duration):
    """
    convert movie duration to standard format in minutes
    duration: str xx h xx m
    """
    print(duration)
    if duration.find('h') != -1:
        hour_part = re.search(r".+(?=h)", duration).group(0).strip()
        if duration.find('m') != -1:
            minute_part = re.search(r"(?<=h).+(?=m)", duration).group(0).strip()
        else:
            minute_part = 0
    else:
        hour_part = 0
        minute_part = re.search(r".+(?=m)", duration).group(0).strip()
    duration = int(hour_part) * 60 + int(minute_part)
    return duration


def review_date_to_datetime(date):
    """
    convert review date to standard Pandas dataframe datetime64 format
    date: str xx/xx/xxxx
    """
    date_obj = datetime.strptime(date, '%d %B %Y')
    iso_date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return iso_date_str


def clean_text(x):
    clean = ' '.join(re.sub("(@([A-Za-z0-9._-]+))|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",
                            x).split())  # remove @mentions, hashtags, urls, and punctuations
    clean = re.sub(r'\d+', '', clean)
    return clean


def tokenization(x):
    pattern = r'\w[\w\',-]*\w'
    tokens = nltk.regexp_tokenize(x, pattern)

    return tokens


# convert csv string to list
def convert_list(x):
    try:
        return eval(x)
    except:
        return x


# preprocess movie metadata and review data
# convert movie duration to standard format in minutes
def duration_converting(df=default_df):
    df['movie_duration'] = df['movie_duration'].apply(movie_duration_to_minutes)
    print(df['movie_duration'])
    print(df.info())


# convert review date to standard Pandas dataframe datetime64 format
def date_converting(df=default_rw):
    df['review_date'] = df['review_date'].apply(review_date_to_datetime)
    df['review_date'] = pd.to_datetime(df['review_date'])
    print(df['review_date'])
    print(df.info())


def preprocess_single_review(df=default_rw):
    date_converting(df)
    df['review_text'] = df['review_text'].apply(clean_text)
    df.to_csv('processed_data/' + df['movie_title'] + '_reviews.csv', index=False)
    print(df)


def preprocess_all_reviews():
    result_df = None
    # iterate through all csv files in the data folder
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            df = pd.read_csv('data/' + file, header=0)
            # preprocess each review file
            preprocess_single_review(df)
            if result_df is None:
                result_df = df
            else:
                result_df = pd.concat([result_df, df])
            # save the preprocessed file to the data folder

    result_df.to_csv('processed_data/all_reviews.csv', index=False)
    return result_df


def check_review_repeating(df=default_df):
    namelist = df.movie_id.tolist()
    print(namelist)
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            print(str(file))
            sdf = pd.read_csv('data/' + file, header=0)
            a = sdf.movie_id[0]
            print(a)
            if a in namelist:
                namelist.remove(a)
            else:
                print(a+'not in list')
    print(namelist)


# print(default_rw.iloc[:, -3].apply(clean_text).head(10))
# print(default_df.iloc[:, -1].sum())
# print(default_df.movie_genres[0])
# print(default_df.movie_genres.head(10))
# print(default_df.movie_genres.apply(convert_list).head(10))
# print(type(default_df.movie_genres.tolist()[0]))
