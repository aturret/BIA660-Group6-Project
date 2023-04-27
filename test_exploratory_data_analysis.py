from exploratory_data_analysis import *
from util import *
import pandas as pd
import pytest

'''
this is a unit test_data file for functions in exploratory_data_analysis.py
'''

default_df = pd.read_csv('test_data/imdb_top250_metadata.csv', header=0)
default_rw = pd.read_csv('test_data/High and Low_reviews.csv', header=0)
all_reviews = pd.read_csv('processed_data/all_reviews.csv', header=0)

agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}


def test_count_movie_year():
    count_movie_year()


def test_ploting():
    cv = count_movie_year()
    ploting(cv)


def test_head_latex():
    print('')
    df = default_df
    print(correlation_analysis(df))


def test_head():
    # df = all_reviews
    df = default_df
    print("\n")
    print(df.head())
    # get the summation
    print(df.info())


def test_get_weighted_average():
    df = all_reviews
    ndf = get_weighted_average(df)
    print(ndf.info())
    correlation_analysis(ndf)


def test_word_cloud():
    df = all_reviews
    word_cloud(df)





pytest
