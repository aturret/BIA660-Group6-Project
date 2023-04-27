import nltk
from nltk.corpus import stopwords
from sklearn.metrics import pairwise_distances
from nltk.stem import SnowballStemmer
import os
import re
from datetime import datetime
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

# basic settings
default_df = pd.read_csv('test_data/imdb_top250_metadata.csv', header=0)
default_rw = pd.read_csv('test_data/High and Low_reviews.csv', header=0)


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


def tokenization(doc):
    pattern = r'\w[\w\',-]*\w'
    tokens = nltk.regexp_tokenize(doc.lower(), pattern)
    stop_words = stopwords.words('english')
    filtered_tokens = [w for w in tokens if w not in stop_words]
    # print(filtered_tokens)
    return filtered_tokens


def stemming(tokens):
    stemmer = SnowballStemmer('english')
    stemmed_tokens = [stemmer.stem(w) for w in tokens]
    # print(stemmed_tokens)
    return stemmed_tokens


def get_tokens(doc):
    tokens = tokenization(doc)
    stemming_tokens = stemming(tokens)
    return stemming_tokens


def get_frequency(tokens):
    freq = nltk.FreqDist(tokens)
    return freq


def get_token_count(doc):
    tokens = tokenization(doc)
    stemming_tokens = stemming(tokens)
    token_count = get_frequency(stemming_tokens)
    return token_count


def get_docs_frequency(docs):
    docs_token = {}
    for idx, doc in enumerate(docs):
        docs_token[idx] = get_token_count(doc)
    return docs_token


def get_frequency_dataframe(docs):
    pd.options.display.float_format = '{:,.2f}'.format
    docs_token = get_docs_frequency(docs)
    dtm = pd.DataFrame.from_dict(docs_token, orient='index')
    dtm = dtm.fillna(0)
    dtm = dtm.sort_index(axis=0)
    tf = dtm.values
    doc_len = tf.sum(axis=1, keepdims=True)
    tf = np.divide(tf, doc_len)
    df = np.where(tf > 0, 1, 0)
    smoothed_idf = np.log(np.divide(len(docs) + 1, np.sum(df, axis=0) + 1)) + 1
    smoothed_tf_idf = tf * smoothed_idf
    similarity = 1 - pairwise_distances(smoothed_tf_idf, metric='cosine')
    # np.argsort(similarity)[:, ::-1][0, 0:2]
    print(similarity)
    return smoothed_tf_idf


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
    # print(df['review_date'])
    # print(df.info())


def preprocess_single_review(df=default_rw, clean=False):
    date_converting(df)
    if clean:
        df['review_text'] = df['review_text'].apply(clean_text)
    # df.to_csv('processed_data/' + df['movie_title'] + '_reviews.csv', index=False)
    print(df)


def preprocess_all_reviews(clean=False):
    result_df = None
    # iterate through all csv files in the data folder
    for file in os.listdir('data'):
        if file.endswith('.csv'):
            df = pd.read_csv('data/' + file, header=0)
            # preprocess each review file
            preprocess_single_review(df, clean=clean)
            if result_df is None:
                result_df = df
            else:
                result_df = pd.concat([result_df, df])
            # save the preprocessed file to the data folder
    result_df.to_csv('all_reviews.csv', index=False)
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
                print(a + 'not in list')
    print(namelist)

