import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

default_df = pd.read_csv('test/imdb_top250_metadata.csv', header=0)


def correlation_analysis(df=default_df):
    numeric_cols = default_df.select_dtypes(include='number')
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
    # ax = df.cylinders.value_counts().sort_index(axis=0).plot.bar(figsize=(6, 4), title="Model count by cylinders")
    # set labels
    # ax.set(ylabel="cylinders", xlabel="model count")
    sns.barplot(x='year', y='model_count', data=df)
    plt.show()
