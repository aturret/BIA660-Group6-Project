from get_functions import *
from util import *

imdb_top250 = 'https://www.imdb.com/chart/top/'
agent_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

top250_links = get_imdb_top250_links(imdb_top250, agent_headers)
top250_df = pd.DataFrame()
imdb_top250_df = pd.read_csv('tweets.csv', header=0)