import os
import requests
import zipfile
import pandas as pd
import sys
import sqlite3
import time

# Festgelegte Namen für die Datein
raw_gdp_name = 'raw_API_NY.GDP.PCAP.CD_DS2_en_csv_v2_9803.csv'
raw_life_expectancy_name = 'raw_Life expectancy at birth (years).csv'
country_csv_name = 'all_countries.csv'

# Define the absolute path to the data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')

STORE_PATH = os.path.join(DATA_DIR, 'data.sqlite')

# Methode die mir die Daten für das GDP pro Kopf herunterlädt
def download_gross_domestic_product_capita():
    # URL der Daten wo ich das zip herunterladen kann
    url = 'https://api.worldbank.org/v2/en/indicator/NY.GDP.PCAP.CD?downloadformat=csv'
    zip_path = os.path.join(DATA_DIR, 'gross_domestic_product_capita.zip')
    max_retries = 3
    attempt = 0

    # Daten herunterladen (3 mal versuchen)
    while attempt <= max_retries:
        try:
            # Zip datei herunterladen
            r = requests.get(url)
            r.raise_for_status() 
            with open(zip_path, 'wb') as f:
                # Daten in das zip schreiben
                f.write(r.content)
            break
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f'Attempt {attempt} failed: {e}')
            if attempt > max_retries:
                raise ValueError('Failed to download the file after multiple attempts.')
            # Kurze Pause bevor man es nochmal versucht.
            time.sleep(2)

    # Zip entpacken und nach den passenden Dateinamen suchen
    secure_counter = 0
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            # Ich interssiere mich nur für Life expectancy at birth (years) (keine Metadaten)
            if 'Metadata' not in file:
                # Daten aus dem zip extrahieren und umbenennen
                zip_ref.extract(file, DATA_DIR)
                os.rename(f'{DATA_DIR}/{file}', f'{DATA_DIR}/{raw_gdp_name}')
                secure_counter += 1
    # Wenn ich mehr als eins gefunden habe, ist was schief gelaufen. Hier müsste man eine neue if bedinfung schreiben, welche nur die relevante Datei extrahiert.
    if secure_counter != 1:
        raise ValueError('Too many files found. Check the zip file.')
    # Das zip wieder entfernen, da es nicht mehr gebraucht wird.
    os.remove(zip_path)


# Methode die mir die Daten für die Lebenserwartung herunterlädt
def download_and_extract_life_expectancy():
    # Die Methode ist sehr ähnlich zu download_gross_domestic_product_capita
    url = 'https://extdataportal.worldbank.org/content/dam/sites/data/gender-data/data/data-gen/zip/indicator/life-expectancy-at-birth-years.zip'
    zip_path = os.path.join(DATA_DIR, 'life-expectancy-at-birth-years.zip')
    max_retries = 3
    attempt = 0

    # Daten herunterladen (3 mal versuchen)
    while attempt <= max_retries:
        try:
            r = requests.get(url)
            r.raise_for_status() 
            with open(zip_path, 'wb') as f:
                f.write(r.content)
            break
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f'Attempt {attempt} failed: {e}')
            if attempt > max_retries:
                raise ValueError('Failed to download the file after multiple attempts.')
            # Kurze Pause bevor man es nochmal versucht.
            time.sleep(2)

    secure_counter = 0
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            # Ich interssiere mich nur für Life expectancy at birth (years)
            if file == 'Life expectancy at birth (years).csv':
                zip_ref.extract(file, DATA_DIR)
                os.rename(f'{DATA_DIR}/{file}', f'{DATA_DIR}/{raw_life_expectancy_name}')
                secure_counter += 1

    if secure_counter != 1:
        raise ValueError('Too many files found. Check the zip file.')
    os.remove(zip_path)


# Methode um die Länder und ihre Reginnamen herunterzuladen um nur die Länder zu erhalten, welche in Amerika liegen.
def download_country_csv():
    url = 'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv'
    max_retries = 3
    attempt = 0

    while attempt <= max_retries:
        try:
            # Lade die CSV-Datei herunter
            r = requests.get(url)
            r.raise_for_status()
            with open(os.path.join(DATA_DIR, country_csv_name), 'wb') as f:
                f.write(r.content)
            break
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f'Attempt {attempt} failed: {e}')
            if attempt > max_retries:
                raise ValueError('Failed to download the file after multiple attempts.')
            time.sleep(2)


# Methode um alle Rohdaten herunterzuladen
def download_all_raw_data():
    download_gross_domestic_product_capita()
    download_and_extract_life_expectancy()
    download_country_csv()

# Methode um die Daten aus dem data Ordner zu löschen
def clean_data():
    for file in os.listdir(DATA_DIR):
        if file == '.gitkeep':
            continue
        os.remove(os.path.join(DATA_DIR, file))


# Diese Methode dient dazu die Daten vorzuverarbeiten.
def prepare_data(store=False):

    # Hilfsmehtode
    def filter_countries(dataframe, countries):
        # Filtere das df so, dass nur noch die Länder enthalten sind, welche in Amerika sind
        filtered_df = dataframe[dataframe['Country Code'].isin(countries)]
        # Entferne Duplikate falls welche vorhanden sein sollten
        filtered_df = filtered_df.drop_duplicates()
        filtered_list = filtered_df['Country Code'].tolist()
        # Finde heraus, welche Länder nicht gefunden wurden
        not_found_countries = set(countries) - set(filtered_list) 
        return filtered_df, not_found_countries

    # CSV Datei einlesen 
    county_df = pd.read_csv(os.path.join(DATA_DIR, country_csv_name))
    # Extrahiere nur die Ländernamen welche auf dem Kontinent Amerika liegen
    # Ich vergleiche küzel (alpha-3), weil die Namen sich unterscheiden und ich so mehr Treffer erhalte.
    american_countries = county_df[county_df['region'] == 'Americas']['alpha-3'].tolist()
    print(f'Found {len(american_countries)} countries in America')

    # Die ersten 4 Zeilen bestehen aus Überschrift
    for file in os.listdir(DATA_DIR):
        print(file)

    print('Reading raw data: ' + raw_gdp_name)
    gdp_df = pd.read_csv(os.path.join(DATA_DIR, raw_gdp_name), skiprows=4)
    # Entferne Spalten, die ich nicht mehr benötige
    gdp_df = gdp_df.drop(columns=['Indicator Name', 'Indicator Code', 'Unnamed: 68'])
    # Jetzt filtern wir die csv-Dateien, weil uns nur die Länder aus Amerika interessieren
    gdp_df_filtered, not_found_countries_gdp = filter_countries(gdp_df, american_countries)

    # Gebe die Ländernamen aus, welche kein Match gefunden haben
    for country in not_found_countries_gdp:
        print(f'Country not found in GDP data: {county_df[county_df["alpha-3"] == country]["name"].values[0]}')
    
    # Das gleiche auch für die Lebenserwartung
    live_exp_df = pd.read_csv(os.path.join(DATA_DIR, raw_life_expectancy_name))
    live_exp_df = live_exp_df.drop(columns=['Indicator Name', 'Indicator Code'])
    # Hier gebe ich nur die Länder rein, welche ich auch bei GDP gefunden habe
    live_exp_df_filtered, not_found_countries_live = filter_countries(live_exp_df, gdp_df_filtered['Country Code'].tolist())

    for country in not_found_countries_live:
        print(f'Country not found in Life expectancy data: {county_df[county_df["alpha-3"] == country]["name"].values[0]}')

    # Jetzt muss man ggf. nochmal filtern, weil in beiden dfs vielleicht unterschiedliche Länder sind.
    remove_in_gdp = set(not_found_countries_live) - set(not_found_countries_gdp)
    if len(remove_in_gdp) > 0:
        print('Correcting GDP data')
        gdp_df_filtered, _ = filter_countries(gdp_df, gdp_df_filtered['Country Code'].tolist() - remove_in_gdp)

    # Ersetzte NAN durch 0.
    # Das ist evtl. nicht optimal, weil in späteren Berechnungen 0 nicht optimal ist. Ich werde Code schreiben, der dann die Daten nimmt wenn sie vorher mal nicht 0 waren. Also z.B. liegt ein GDP im Jahr 2022 nicht vor, aber 2021 war es bekannt. Dann schriebe ich in 2022 das GDP von 2021.
    print(f'Missing values in GDP data: {gdp_df_filtered.isnull().sum().sum()}')
    print(f'Missing values in Life expectancy data: {live_exp_df_filtered.isnull().sum().sum()}')
    gdp_df_filtered = gdp_df_filtered.fillna(0)
    live_exp_df_filtered = live_exp_df_filtered.fillna(0)


    # Jetzt haben wir "saubere" Daten. In beiden Datensätzen sind länder aus Amerika enthalten und auch in beiden die gleichen Länder.
    if store:
        # Die Daten werden jetzt in data.sqlite gespeichert
        conn = sqlite3.connect(STORE_PATH)
        gdp_df_filtered.to_sql('gdp_data', conn, if_exists='replace', index=False)
        live_exp_df_filtered.to_sql('life_expectancy_data', conn, if_exists='replace', index=False)
        conn.close()
    return gdp_df_filtered, live_exp_df_filtered


if __name__ == '__main__':
    # Ich möchte das mind. ein argument übergeben wird
    if len(sys.argv) == 1:
        print('Please provide an argument. Use "download" to download the raw data or "prepare" to prepare the data.')
        sys.exit()

    # Erstelle den data Ordner falls er nicht existiert
    if not os.path.exists('../data'):
        os.makedirs('../data')

    # Daten aus dem Ordner löschen
    if 'clean' in sys.argv:
        clean_data()
        print('Data cleaned')
    
    # Rohdaten herunterladen
    if 'download' in sys.argv:
        download_all_raw_data()
        print('Data downloaded')

    # Daten vorverarbeiten und als sqlite abspeichern
    if 'prepare' in sys.argv:
        prepare_data(store=True)
        print('Data prepared')

    # Argument zum ausgeben von testdaten aus der Sqlite
    if 'test' in sys.argv:
        conn = sqlite3.connect(STORE_PATH)
        df = pd.read_sql('SELECT * FROM gdp_data', conn)
        print(df.head())
        df = pd.read_sql('SELECT * FROM life_expectancy_data', conn)
        print(df.head())
        conn.close()
        print('Data read from sqlite')
