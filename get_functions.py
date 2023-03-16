import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from util import *

single_movie_col = ['movie_id', 'movie_title', 'movie_rating', 'movie_rating_number', 'movie_genres', 'movie_year',
                    'movie_content_rating', 'movie_duration', 'movie_reviews_link', 'review_number']
single_review_col = ['movie_id', 'movie_title', 'review_id', 'review_author', 'review_title', 'review_date',
                     'review_rating',
                     'review_text', 'review_helpfulness_upvote', 'review_helpfulness_total']


def get_imdb_top250_links(url, headers):
    movie_links: list[str] = []
    try:
        imdb_top250_page = requests.get(url, headers=headers)
        if imdb_top250_page.status_code == 200:
            imdb_top250_soup = BeautifulSoup(imdb_top250_page.content, 'html.parser')
            movie_list = imdb_top250_soup.find('tbody').find_all('tr')
            for i in movie_list:
                movie_link = i.find('a').get('href')
                movie_link = 'https://www.imdb.com' + movie_link
                # clean the link, remove '?pf_rd_m='
                movie_link = re.sub(r'\?pf_rd_m=.*', '', movie_link)
                movie_links.append(movie_link)
    except Exception as e:
        print(e)
    return movie_links


def get_single_movie_info(url, headers, method='requests', col=None):
    if col is None:
        col = single_movie_col
    print(url)
    movie_info = []
    movie_page = None
    try:
        if method == 'Selenium':
            movie_page = get_page_by_selenium(url, 10)
        elif method == 'requests':
            movie_page = requests.get(url, headers=headers).content
        if movie_page:
            movie_soup = BeautifulSoup(movie_page, 'html.parser')
        else:
            raise Exception('movie_page is None')
        # print(movie_soup)
        movie_id = re.search(r"title", url).group(0)
        movie_title = movie_soup.find('h1').text
        movie_rating = movie_soup.find('div', attrs={'data-testid': 'hero-rating-bar__aggregate-rating__score'}).find(
            'span').text
        movie_rating_page_link = 'https://www.imdb.com' + movie_soup.find('div', attrs={
            'data-testid': 'hero-rating-bar__aggregate-rating'}).find('a').get('href')
        movie_ratings_info = get_single_movie_ratings_info(movie_rating_page_link, headers)
        movie_rating_number = movie_ratings_info[0]
        # print(movie_rating_number)
        movie_genres_list = movie_soup.find("div", attrs={'class': 'ipc-chip-list__scroller'}).find_all('a')
        movie_genres = []
        for genre in movie_genres_list:
            movie_genres.append(genre.find('span').text)
        # print(movie_genres)
        try:
            movie_title_siblings = movie_soup.find('h1').find_next_siblings()
            if movie_title_siblings[0].find_all():
                movie_basic_info_list = movie_title_siblings[0].find_all('li')
            else:
                movie_basic_info_list = movie_title_siblings[1].find_all('li')
            movie_year = movie_basic_info_list[0].find('a').text if movie_basic_info_list[0].find('a') else None
            movie_content_rating = movie_basic_info_list[1].find('a').text if movie_basic_info_list[1].find('a') else None
            movie_duration = movie_basic_info_list[2].text if len(movie_basic_info_list)>2 else None
        except Exception as e:
            print(e)
            with open('test/'+movie_title+'.html', 'w', encoding="utf-8") as f:
                f.write(movie_page.decode('utf-8'))
            pass
            raise Exception('movie_basic_info_list error')
        movie_reviews_link = 'https://imdb.com' + re.sub(r'\?ref_=.*', '', movie_soup.find("section", attrs={
            'data-testid': 'UserReviews'}) \
                                                         .find('a', class_='ipc-title-link-wrapper').get('href'))
        review_number = get_single_movie_reviews_info(movie_reviews_link, headers)[0]
        movie_info = [movie_id, movie_title, movie_rating, movie_rating_number, movie_genres, movie_year,
                      movie_content_rating, movie_duration, movie_reviews_link, review_number]
        print(movie_info)
    except Exception as e:
        print(e)
    return movie_info


def get_single_movie_ratings_info(url, headers):
    movie_ratings_info = []
    try:
        movie_ratings_page = requests.get(url, headers=headers)
        if movie_ratings_page.status_code == 200:
            movie_ratings_soup = BeautifulSoup(movie_ratings_page.content, 'html.parser')
            movie_ratings_number = re.compile(r'[^0-9]+').sub('', re.search(r"(.*)\s+(IMDb users)",
                                                                            movie_ratings_soup.find('div',
                                                                                                    class_='allText').find_all(
                                                                                'div')[0].text).group(1))
        else:
            raise Exception('movie_ratings_page status code is not 200')
        movie_ratings_info = [movie_ratings_number]
    except Exception as e:
        print(e)
    return movie_ratings_info


def get_single_movie_reviews_info(url, headers):
    movie_reviews_info = []
    try:
        movie_reviews_page = requests.get(url, headers=headers)
        if movie_reviews_page.status_code == 200:
            movie_reviews_soup = BeautifulSoup(movie_reviews_page.content, 'html.parser')
            reviews_header = movie_reviews_soup.find('section', class_='article').find('div', class_='header').find(
                'span')
            movie_reviews_number = re.compile(r'[^0-9]+').sub('', reviews_header.text)
        else:
            raise Exception('movie_reviews_page status code is not 200')
        movie_reviews_info = [movie_reviews_number]
    except Exception as e:
        print(e)
    return movie_reviews_info


def get_imdb_top250_metadata(movie_links, headers, method='requests'):
    data = []
    col = ['movie_id', 'movie_title', 'movie_rating', 'movie_rating_number', 'movie_genres', 'movie_year',
           'movie_content_rating', 'movie_duration', 'movie_reviews_link', 'review_number']
    for link in movie_links:
        data.append(get_single_movie_info(link, headers, method=method))
    write_csv_file(filename='imdb_top250_metadata.csv', columns=col, records=data)
    metadata = pd.DataFrame(data, columns=col)
    return metadata


def get_review_links(reviews_link, headers):
    review_links = []
    # Selenium initialization
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={headers["User-Agent"]}')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--allow-running-insecure-content')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(reviews_link)
        while True:
            try:
            # next_page = driver.find_elements()[0]
                wait = WebDriverWait(driver, 3)
                button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ipl-load-more__button']")))
                if button:
                    # print('clicking button')
                    button.click()
                    time.sleep(1)
                else:
                    print('no more button')
                    break
            except Exception as e:
                print(e)
                break
        reviews_page = driver.page_source
        reviews_soup = BeautifulSoup(reviews_page, 'html.parser')
        reviews = reviews_soup.find('div', class_='lister-list').find_all('div', {'class': ['lister-item', 'mode-detail','imdb-user-review']} )
        for review in reviews:
            review_link = re.sub(r'\?ref_=.*', '', 'https://imdb.com' + review.find('a').get('href'))
            review_links.append(review_link)
        print(len(review_links))
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return review_links


def get_single_review(review_link, headers):
    review = []
    try:
        review_page = requests.get(review_link, headers=headers)
        if review_page.status_code == 200:
            review_soup = BeautifulSoup(review_page.content, 'html.parser')
            # get review data
            movie_id = review_soup.find('div', class_='lister-item-header').find('a').get('href').split('/')[2]
            movie_title = review_soup.find('div', class_='lister-item-header').find('a').text
            review_id = review_link.split('/')[4]
            review_author = review_soup.find('h3').find('a').text
            review_title = review_soup.find('a', class_='title').text
            review_date = review_soup.find('div', class_='display-name-date').find('span').text
            review_rating = review_soup.find('span', class_='rating-other-user-rating').find('span').text if \
                review_soup.find('span', class_='rating-other-user-rating') else None
            review_text = review_soup.find('div', class_='text show-more__control').text
            review_helpfulness = review_soup.find('div', class_='actions text-muted').text
            review_helpfulness_upvote = re.compile(r'.+(?=out)').search(review_helpfulness).group(0).strip()
            review_helpfulness_total = re.compile(r'(?<=of).+(?=found)').search(review_helpfulness).group(0).strip()
            review = [movie_id, movie_title, review_id, review_author, review_title, review_date, review_rating,
                      review_text, review_helpfulness_upvote, review_helpfulness_total]
        else:
            raise Exception('review_page status code is not 200')
    except Exception as e:
        print(e)
    return review


def get_all_reviews_of_single_movie(reviews_link, headers, col=None):
    if col is None:
        col = single_review_col
    review_links = get_review_links(reviews_link, headers)
    data = []
    for link in review_links:
        data.append(get_single_review(link, headers))
    title = data[0][1]
    write_csv_file(filename='data/'+title+'_reviews.csv', columns=col, records=data)
    reviews = pd.DataFrame(data, columns=col)
    return reviews

def get_all_reviews_of_all_movies(metadata, headers, col=None):
    if col is None:
        col = single_review_col
    for index, row in metadata.iterrows():
        reviews_link = row['movie_reviews_link']
        reviews = get_all_reviews_of_single_movie(reviews_link, headers, col=col)
