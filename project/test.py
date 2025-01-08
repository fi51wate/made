import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import os

INTERPOLATE = True

DATA_DIR = os.path.join(os.getcwd(), '../data/data.sqlite')
conn = sqlite3.connect(DATA_DIR)
df_gdp = pd.read_sql_query('SELECT * FROM gdp_data', conn)
df_live = pd.read_sql_query('SELECT * FROM life_expectancy_data', conn)

print(df_live.head())

genders = df_live.groupby('Disaggregation')
for gender in genders:
    plt.figure(figsize=(15, 8))
    for group in gender[1].groupby('Country Code'):
        plt.plot(group[1]['Value'].values, label=group[0])