import pandas as pd
import sqlite3
import glob
import os

def clean_data(df):

    # puste miejsca w bazie wypełniamy gdzie ma to sens
    df['type'] = df['type'].fillna('unknown')
    df['buildingMaterial'] = df['buildingMaterial'].fillna('other')
    df['hasElevator'] = df['hasElevator'].fillna('no')
    
    # zmieniamy dane z no i yes na 0 i 1
    columns_to_change = ['hasParkingSpace', 'hasBalcony', 'hasSecurity','hasStorageRoom','hasElevator']
    maping = {'yes': 1, 'no': 0}
    df[columns_to_change] = df[columns_to_change].applymap(lambda x: maping.get(x, x))


    # usuwanie niepotrzebnych kolumn / kolumn z dużą ilością nulli
    rare_columns = ['clinicDistance','kindergartenDistance','condition','longitude', 'latitude',
                    'restaurantDistance','pharmacyDistance','postOfficeDistance','ownership']
    df.drop(columns=rare_columns, inplace=True)

    return df

def load_data_to_sqlite():

    data_directory = './data'
    conn = sqlite3.connect('apartments.db')

    # Wczytanie plików ze sprzedażą mieszkań
    sale_files = glob.glob(os.path.join(data_directory, 'apartments_pl_*.csv'))
    
    # Pobranie wszystkich tabel w bazie danych
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Usunięcie każdej tabeli
    for table in tables:
        table_name = table[0]
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Tabela {table_name} została usunięta.")
    
    for file in sale_files:
        # Wczytanie danych
        df = pd.read_csv(file)

        # CZYSZCZENIE DANYCH
        # Puste miejsca w bazie wypełniamy gdzie ma to sens
        df['type'] = df['type'].fillna('unknown')
        df['buildingMaterial'] = df['buildingMaterial'].fillna('other')
        df['hasElevator'] = df['hasElevator'].fillna('no')

        # Zamieniamy dane z 'no' i 'yes' na 0 i 1
        columns_to_change = ['hasParkingSpace', 'hasBalcony', 'hasSecurity','hasStorageRoom','hasElevator']
        maping = {'yes': 1, 'no': 0}
        df[columns_to_change] = df[columns_to_change].map(lambda x: maping.get(x, x))


        # Usuwanie niepotrzebnych kolumn / kolumn z dużą ilością nulli
        rare_columns = ['clinicDistance','kindergartenDistance','condition','longitude', 'latitude',
                        'restaurantDistance','pharmacyDistance','postOfficeDistance','ownership']
        df = df.drop(columns=rare_columns)

        # Dodanie kolumny z datą (z nazwy pliku)
        filename = os.path.basename(file)
        date = filename.split('_')[2:4]  # Wyciąga YYYY_MM z nazwy
        df['date'] = f"{date[0]}-{date[1].split('.')[0]}"

        # Zapis do bazy
        df.to_sql('apartments_sale', conn, if_exists='append', index=False)

    # Tworzenie indeksów dla często używanych kolumn
    cursor = conn.cursor()
    

    cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_apartments_sale_city 
        ON apartments_sale(city)
    """)
    cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_apartments_sale_date 
        ON apartments_sale(date)
    """)

    conn.commit()
    conn.close()
    
    print("Dane wczytane poprawnie!")


if __name__ == "__main__":
    load_data_to_sqlite()
