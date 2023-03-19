from exploratory_data_analysis import *
from util import *
import pandas as pd
import pytest

'''
this is a unit test file for functions in get_functions.py
'''

agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}


def test_count_movie_year():
    count_movie_year()


def test_ploting():
    cv = count_movie_year()
    ploting(cv)




pytest
