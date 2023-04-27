from classification import *
from util import *
import pandas as pd
import pytest

'''
this is a unit test_data file for functions in classification.py
'''
default_df = pd.read_csv('test_data/imdb_top250_metadata.csv', header=0)
default_rw = pd.read_csv('test_data/High and Low_reviews.csv', header=0)
all_reviews = pd.read_csv('processed_data/all_reviews.csv', header=0)
agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

# dtm = label_reviews(default_rw)
dtm = label_reviews(all_reviews)
x_train, x_test, y_train, y_test = train_test_split(dtm['review_text'], dtm['label'], test_size=0.3, random_state=0)


def test_label_reviews():
    print('')
    rw = default_rw
    df = label_reviews(rw)
    print(df)


def test_create_model():
    print('')
    # auc_score, prc_socre = create_model(x_train, y_train, x_test, y_test,
    #                                     model_type='svm', min_df=1, stop_words=None,
    #                                     print_result=True, algorithm_para=1.0)
    auc_score, prc_socre = create_model(x_train, y_train, x_test, y_test,
                                        model_type='svm', min_df=1, stop_words=None,
                                        print_result=True, algorithm_para=0.5)


def test_search_para():
    print('')
    search_para(x_train, y_train)


def test_sample_size_impact():
    print('')
    sample_size_impact(x_train, y_train)


def test_helpfulness_label_model():
    print('')
    df = get_helpfulness_rate(all_reviews)
    df = label_reviews(df,'review_text','helpfulness_rate')
    x_train, x_test, y_train, y_test = train_test_split(df['review_text'], df['label'], test_size=0.3, random_state=0)
    create_model(x_train, y_train, x_test, y_test, model_type='svm', min_df=1, stop_words=None,
                                        print_result=True, algorithm_para=0.5)


pytest
