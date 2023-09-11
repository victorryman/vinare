import os
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

country_names_mapping = {
    'Tyskland': 'Germany',
    'Spanien': 'Spain',
    'Italien': 'Italy',
    'Frankrike': 'France',
    'Sydafrika': 'South Africa',
    'EU': 'European Union',
    'Argentina': 'Argentina',
    'Ungern': 'Hungary',
    'Sverige': 'Sweden',
    'Nya Zeeland': 'New Zealand',
    'Internationellt märke': 'International Brand',
    'Portugal': 'Portugal',
    'Australien': 'Australia',
    'Chile': 'Chile',
    'Moldavien': 'Moldova',
    'Österrike': 'Austria',
    'Danmark': 'Denmark',
    'USA': 'United States',
    'Grekland': 'Greece',
    'Kosovo': 'Kosovo',
    'Rumänien': 'Romania',
    'Belarus': 'Belarus',
    'Serbien': 'Serbia',
    'Storbritannien': 'United Kingdom',
    'Slovenien': 'Slovenia',
    'Slovakien': 'Slovakia',
    'Tjeckien': 'Czech Republic',
    'Golanhöjderna (israelisk bosättning)': 'Golan Heights (Israeli Settlement)',
    'Georgien': 'Georgia',
    'Bulgarien': 'Bulgaria',
    'Kroatien': 'Croatia',
    'Ukraina': 'Ukraine',
    'Turkiet': 'Turkey',
    'Libanon': 'Lebanon',
    'Armenien': 'Armenia',
    'Cypern': 'Cyprus',
    'Nordmakedonien': 'North Macedonia',
    'Israel': 'Israel',
    'Schweiz': 'Switzerland',
    'Varierande ursprung': 'Various Origins',
    'Uruguay': 'Uruguay',
    'Mexiko': 'Mexico',
    'Montenegro': 'Montenegro',
    'Peru': 'Peru',
    'Marocko': 'Morocco',
    'Lodi': 'Lodi',
    'Japan': 'Japan',
    'Bosnien-Hercegovina': 'Bosnia and Herzegovina',
    'Kanada': 'Canada',
    'Serbien och Montenegro': 'Serbia and Montenegro',
    'Nederländerna': 'Netherlands'
}

# Define the folder path
folder_path = 'wines'

# Initialize an empty list to store DataFrames
dfs = []

# Walk through the folder and its sub-folders
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            df = pd.read_csv(file_path)
            wine_type = file.split('-')[0]
            df['type'] = wine_type.title()
            dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
final_df = pd.concat(dfs, ignore_index=True)
final_df['art_nr'] = final_df['art_nr'].str.replace('Nr ', '')
final_df['volume'] = final_df['volume'].str.replace(' ml', '')
final_df['volume'] = final_df['volume'].str.replace(' ', '')
final_df = final_df.dropna(subset=['volume'])
final_df['volume'] = pd.to_numeric(final_df['volume'], errors='coerce')
final_df['alc_vol'] = final_df['alc_vol'].str.replace(' % vol.', '').str.replace(',', '.')
final_df['price'] = final_df['price'].str.replace(':-', '')
final_df['price'] = final_df['price'].str.replace(' ', '')
final_df['price'] = final_df['price'].str.replace('*', '')
final_df['price'] = final_df['price'].str.replace(':', '.')
final_df['country'] = final_df['country'].map(country_names_mapping)
final_df = final_df.drop_duplicates()

snapdate = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
final_df.insert(0, 'snapdate', snapdate)

final_df.to_csv(f'alla_viner_{snapdate.date()}.csv', index=False)
