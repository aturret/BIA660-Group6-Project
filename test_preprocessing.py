from preprocessing import *
from util import *
import pandas as pd
import pytest

'''
this is a unit test file for functions in get_functions.py
'''

agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}


def test_movie_duration_to_minutes():
    duration = '2 h 22 min'
    assert movie_duration_to_minutes(duration) == 142


def test_duration_converting():
    duration_converting()


def test_review_date_to_datetime():
    date = '1 January 2000'
    assert review_date_to_datetime(date) == '2000-01-01 00:00:00'


def test_date_converting():
    date_converting()


def test_preprocess_single_review():
    # test_review = ''
    preprocess_single_review()




pytest
