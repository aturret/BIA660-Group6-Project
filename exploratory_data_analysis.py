import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import collections
import preprocessing
from wordcloud import WordCloud
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
default_df = pd.read_csv('test_data/imdb_top250_metadata.csv', header=0)
default_rw = pd.read_csv('test_data/High and Low_reviews.csv', header=0)


def correlation_analysis(df=default_df):
    numeric_cols = df.select_dtypes(include='number')
    corr_matrix = numeric_cols.corr()
    print(corr_matrix)
    return corr_matrix


def count_movie_year(df=default_df):
    df['decade'] = df['movie_year'].apply(lambda x: int(x / 10) * 10)
    decade_counts = df['decade'].value_counts().sort_index()
    decade_counts.columns = ["year", "model_count"]
    print(decade_counts)
    return decade_counts


def ploting(df):
    sns.barplot(x='year', y='model_count', data=df)
    plt.show()


def word_cloud(df):
    wc = WordCloud(
        max_words=25,
        max_font_size=100,
        width=1000,
        height=600,
        margin=0
    )
    df['review_token'] = df['review_text'].apply(lambda x: preprocessing.get_tokens(x))
    # combine all tokens into one list for word cloud
    all_tokens = []
    for tokens in df['review_token']:
        all_tokens += tokens
    word_counts = collections.Counter(all_tokens)
    wc.generate_from_frequencies(word_counts)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()


def get_weighted_average(df):
    df = df[df['review_rating'].notnull()]
    # review_count = df.groupby('movie_id')['review_id'].count()
    review_count = df['review_id'].count()
    # rating_sum = df.groupby('movie_id')['review_rating'].sum()
    rating_sum = df['review_rating'].sum()
    weighted_average = rating_sum / review_count
    median_rating = df['review_rating'].median()
    print('average:', weighted_average)
    print("median:", median_rating)
    # keep the same sequence as the original df
    movie_stats = df.groupby('movie_id').agg(
        movie_average_rating=('review_rating', 'mean'),
        movie_total_reviews=('review_id', 'count')
    ).reset_index()
    # join with the original df by movie_id
    movie_stats = default_df.merge(movie_stats, on='movie_id', how='left')
    # movie_stats = movie_stats.merge(default_df[['movie_id', 'movie_title', 'movie_rating']],
    #                                 on='movie_id', how='left')
    # sort by average rating
    # movie_stats = movie_stats.sort_values(by='movie_average_rating', ascending=False)
    print(movie_stats.head(10))
    return movie_stats
    # print(weighted_average.sort_values(ascending=False).head(10))


