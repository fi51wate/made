import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import os

# Set this to False if you want to see the raw data without interpolation
INTERPOLATE = True
DISABLE_TAX_HAVENS = True

TAX_HAVENS = ['CYM', 'BMU']

DATA_DIR = os.path.join(os.getcwd(), '../data/data.sqlite')
conn = sqlite3.connect(DATA_DIR)
df_gdp = pd.read_sql_query('SELECT * FROM gdp_data', conn)
df_live_male = pd.read_sql_query('SELECT * FROM life_expectancy_data_male', conn)
df_live_female = pd.read_sql_query('SELECT * FROM life_expectancy_data_female', conn)
df_live_total = pd.read_sql_query('SELECT * FROM life_expectancy_data_total', conn)

# df_gdp.head()
# df_live_male.head()
# df_live_female.head()
# df_live_total.head()

def interpolate(dataframe):
    # Yeah you see right I did a lot of effort to do this!
    years = dataframe.select_dtypes(include='number').columns
    data = []
    avg_growth = np.zeros(len(years))
    avg_counter = np.zeros(len(years))
    # Iterate over each Country
    for index, row in dataframe.iterrows():
        split = []
        timeline = []
        start = False
        last_year = 0
        for i, year in enumerate(years):
            split.append(row[year])
            # Here we calculate the gradient of the growth as described in Preparation
            if last_year != 0 and row[year] != 0:
                avg_growth[i] += row[year] / last_year
                avg_counter[i] += 1
            last_year = row[year]

            # We create "timelines" that means lines where we have valid data
            if row[year] == 0 and i == 0:
                start = True
            elif row[year] != 0:
                if start and len(timeline) == 0:
                    timeline.append(np.array(split))
                    split = []
        timeline.append(np.array(split))
        data.append(timeline)
    for i in range(1, len(avg_growth)):
        avg_growth[i] /= avg_counter[i]

    new_data = []
    # Here we connect the timelines and fill with the average growth in between
    for timeline in data:
        if len(timeline) > 1:
            if timeline[0][0] == 0:
                if timeline[0][-1] == 0:
                    print('Invalid timeline: ' + str(timeline))
                for i in reversed(range(len(timeline[0]) - 1)):
                    if timeline[0][i] == 0:
                        timeline[0][i] = timeline[0][i + 1] / avg_growth[i + 1]
                    else:
                        print('Interpolating A')
            new_data.append(np.concatenate([timeline[0], timeline[1]]))
        else:
            new_data.append(timeline[0])

    index = 0
    # Write values back to df
    for timeline in new_data:
        for i in range(1, len(timeline)):
            if timeline[i] == 0:
                timeline[i] = timeline[i - 1] * avg_growth[i]

        if index >= len(dataframe):
            print('Index out of bounds')
            break
        
        for j, year in enumerate(years):
            if dataframe.at[index, year] == 0:
                dataframe.at[index, year] = timeline[j]
        index += 1
    return dataframe

if DISABLE_TAX_HAVENS:
    df_gdp = df_gdp[~df_gdp['Country Code'].isin(TAX_HAVENS)]
    df_live_male = df_live_male[~df_live_male['Country Code'].isin(TAX_HAVENS)]
    df_live_female = df_live_female[~df_live_female['Country Code'].isin(TAX_HAVENS)]
    df_live_total = df_live_total[~df_live_total['Country Code'].isin(TAX_HAVENS)]


if INTERPOLATE:
    df_gdp = interpolate(df_gdp)
    df_live_male = interpolate(df_live_male)
    df_live_female = interpolate(df_live_female)
    df_live_total = interpolate(df_live_total)

# Sort the data after best Value in the last comlumn for labels of the plotes to make it more readable
df_gdp = df_gdp.sort_values(by=df_gdp.columns[-1], ascending=False)
df_live_male = df_live_male.sort_values(by=df_live_male.columns[-1], ascending=False)
df_live_female = df_live_female.sort_values(by=df_live_female.columns[-1], ascending=False)
df_live_total = df_live_total.sort_values(by=df_live_total.columns[-1], ascending=False)
# df_gdp.head()
# df_live_male.head()
# df_live_female.head()
# df_live_total.head()