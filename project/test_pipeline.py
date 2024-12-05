import pandas as pd
import sqlite3
import sys
import datapipline as dp
import os

def test_create_data():
    dp.clean_data()
    dp.download_all_raw_data()
    dp.prepare_data(True)

    # Check if the data is created
    assert os.path.exists(f'{dp.STORE_PATH}')


def test_load_data():
    try:
        conn = sqlite3.connect(f'{dp.STORE_PATH}')

        # Check if the required tables exist
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if 'gdp_data' not in [tableName[0] for tableName in tables]:
            print("Missing table 'gdp_data' in sqlite")
            return None, None

        if 'life_expectancy_data' not in [tableName[0] for tableName in tables]:
            print("Missing table 'life_expectancy_data' in sqlite")
            return None, None

        # Load the data
        df_gdp = pd.read_sql_query('SELECT * FROM gdp_data', conn)
        df_live = pd.read_sql_query('SELECT * FROM life_expectancy_data', conn)
        return df_gdp, df_live
    except sqlite3.Error as e:
        print(f"Failed to connect to SQLite: {e}")
    finally:
        if conn:
            conn.close()


def test_structure(df_gdp, df_live):
    # Check if the data has nessary columns
    min_gdp_colums = ['Country Name', 'Country Code']
    if not all(item in df_gdp.columns for item in min_gdp_colums):
        print(f"Missing columns in gdp_data: {min_gdp_colums}")
        return False
    
    # I need at least 5 years
    if df_gdp.columns.size < 7:
        print(f"Missing columns in gdp_data: {df_gdp.columns}")
        return False

    for column in df_gdp.columns[2:]:
        # Check if the column is a number
        number = int(column)
        # I think in the years 1000 there exists no data xD
        if number < 1000:
            print(f"Invalid year in gdp_data: {number}")
            return False

    min_live_columns = ['Country Name', 'Country Code', 'Year', 'Value', 'Disaggregation']
    if not all(item in df_live.columns for item in min_live_columns):
        print(f"Missing columns in life_expectancy_data: {min_live_columns}")
        return False

    return True
    

def test_content(df_gdp, df_live):
    # Check county code:
    for code in df_gdp['Country Code']:
        if len(code) != 3:
            print(f"Invalid country code: {code}")
            return False
    
    # Check if the GDP values are valid
    for col in df_gdp.columns[2:]:
        for value in df_gdp[col]:
            number = float(value)
            if number < 0:
                print(f"Invalid GDP value: {number}")
                return False

    # Check if the life expectancy values are valid
    for code in df_live['Country Code']:
        if len(code) != 3:
            print(f"Invalid country code: {code}")
            return False

    # Check if the year and value are valid
    for year in df_live['Year']:
        if year < 1000:
            print(f"Invalid year: {year}")
            return False
    
    # Check if the value is valid
    for value in df_live['Value']:
        if value < 0:
            print(f"Invalid life expectancy value: {number}")
            return False

    # Check if the disaggregation have at least the values which i need for my analysis
    required_values = {'male', 'female', 'total'}
    disaggregation_values = set(df_live['Disaggregation'].dropna().unique())
    
    if not required_values.intersection(disaggregation_values):
        print("The 'Disaggregation' column does not contain 'male', 'female', or 'total'.")

    return True


if __name__ == '__main__':
    # Create the date first
    test_create_data()

    # Load the data
    df_gdp, df_live = test_load_data()

    if df_gdp is None or df_live is None:
        print("Failed to load the data.")
        sys.exit(1)
    else:
        print("Data loaded successfully.")

    # Test the structure of the tables
    result = test_structure(df_gdp, df_live)

    if result:
        print("Passed the structure test.")
    else:
        print("Failed the structure test.")
        sys.exit(1)

    # Test the content of the tables
    result = test_content(df_gdp, df_live)
    if result:
        print("Passed the content test.")
    else:
        print("Failed the content test.")
        sys.exit(1)

    print("All tests passed.")
