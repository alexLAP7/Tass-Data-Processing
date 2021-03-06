import numpy as np
import time
import pandas as pd
import pickle


class Cleaner:
    def __init__(self, list_of_paths):
        super().__init__()
        self.list_of_paths = list_of_paths
        self.df = None
        self.init()
        # print(self.df.head())

    def init(self):
        list_of_df = []
        for i, path in enumerate(self.list_of_paths):
            with open(path, 'rb') as f:
                data = pickle.load(f)
            list_of_df.append(pd.DataFrame(data))
        self.df = pd.concat(list_of_df, ignore_index=True)

    def save_df_as_image(self, path_to_save_the_image):
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        matplotlib.style.use('ggplot')
        import seaborn as sns
        matplotlib.rcParams['figure.figsize'] = (20, 20)  # (12,8)

        print('visualizing...')
        cols = self.df.columns
        colors = ['#b00b69', '#2b2b2b']  # 9e9e9e
        sns_plot = sns.heatmap(
            self.df[cols].isnull(), cmap=sns.color_palette(colors))
        print('...going to save the image...')

        fig = sns_plot.get_figure()
        fig.savefig(path_to_save_the_image + ".png")
        print('...saved')

    def save_df_as_csv(self, path_to_save_the_df):
        # self.df.head(100).to_csv('data/df_head_100.csv')
        # self.df.to_csv('data/cleared_data.csv')  # ~160Mb
        self.df.to_csv(path_to_save_the_df + '.csv')

    def drop_redundant_data(self):
        df = self.df

        print('original shape:')
        print(df.shape)

        print('deleted all duplicates:')
        df = df.loc[~df.timestamp.duplicated(keep='first')]
        print(df.shape)

        print('deleted all items without an article:')
        df = df[df.article_text.notnull()]
        print(df.shape)

        self.df = df

    def show_basic_info(self):
        df = self.df
        print(df.shape)
        print(df.dtypes)

        df_numeric = df.select_dtypes(include=[np.number])
        numeric_cols = df_numeric.columns.values
        print(numeric_cols)

        df_non_numeric = df.select_dtypes(exclude=[np.number])
        non_numeric_cols = df_non_numeric.columns.values
        print(non_numeric_cols)
