import pandas as pd
import sqlite3
import glob
import os
import numpy as np

def clean_data(df):

    # puste miejsca w bazie wypełniamy
    df['hasElevator'].fillna('no', inplace=True)

    # zmieniamy dane z no i yes na 0 i 1
    columns_to_change = ['hasParkingSpace', 'hasBalcony', 'hasSecurity','hasStorageRoom','hasElevator']
    maping = {'yes': 1, 'no': 0}
    df[columns_to_change] = df[columns_to_change].applymap(lambda x: maping.get(x, x))


    # usuwanie niepotrzebnych kolumn i kolumn z dużą ilością nulli
    rare_columns = ['clinicDistance','kindergartenDistance','condition',
                    'restaurantDistance','pharmacyDistance','postOfficeDistance','ownership']
    df.drop(columns=rare_columns, inplace=True)


    # nulle zastępujemy medianą danej kolumny
    median_floor = df['floor'].median()
    median_floorCount = df['floorCount'].median()
    df['floor'].fillna(median_floor, inplace=True)
    df['floorCount'].fillna(median_floorCount, inplace=True)

    return df

def load_data_to_sqlite(data_directory, db_name='apartments.db'):

    conn = sqlite3.connect(db_name)
    
    # Wczytanie plików ze sprzedażą mieszkań
    sale_files = glob.glob(os.path.join(data_directory, 'apartments_pl_*.csv'))
    
    for file in sale_files:
        # Wczytanie danych
        df = pd.read_csv(file)
        
        # Czyszczenie danych
        df = clean_data(df)
        
        # Dodanie kolumny z datą (z nazwy pliku)
        filename = os.path.basename(file)
        date = filename.split('_')[2:4]  # Wyciąga YYYY_MM z nazwy
        df['date'] = f"{date[0]}-{date[1].split('.')[0]}"
        
        # Zapis do bazy
        df.to_sql('apartments_sale', conn, if_exists='append', index=False)
    
    # Wczytanie plików z wynajmem mieszkań
    rent_files = glob.glob(os.path.join(data_directory, 'apartments_rent_pl_*.csv'))
    
    for file in rent_files:
        # Wczytanie danych
        df = pd.read_csv(file)
        
        # Czyszczenie danych
        df = clean_data(df)
        
        # Dodanie kolumny z datą (z nazwy pliku)
        filename = os.path.basename(file)
        date = filename.split('_')[3:5]  # Wyciąga YYYY_MM z nazwy
        df['date'] = f"{date[0]}-{date[1].split('.')[0]}"
        
        # Zapis do bazy
        df.to_sql('apartments_rent', conn, if_exists='append', index=False)
    
    # Tworzenie indeksów dla często używanych kolumn
    cursor = conn.cursor()
    
    for table in ['apartments_sale', 'apartments_rent']:
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{table}_city 
            ON {table}(city)
        """)
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{table}_price 
            ON {table}(price)
        """)
        cursor.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_{table}_date 
            ON {table}(date)
        """)
    
    conn.commit()
    conn.close()
    
    print("Dane wczytane poprawnie!")




if __name__ == "__main__":
    data_dir = "./data"
    load_data_to_sqlite(data_dir)
