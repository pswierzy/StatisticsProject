import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import numpy as np

def desribe_important(df):
    important_columns = ['price', 'squareMeters', 'rooms', 'buildYear', 'floor', 'floorCount']
    stats = df[important_columns].describe().round(2)
    print(stats)

def num_in_cities(df):
    plt.figure(figsize = (10,5))
    df = df.groupby(['city'])['price'].count().reset_index()
    df = df.sort_values(by = 'price')

    plt.xlabel('Miasto')
    plt.ylabel('Ilość mieszkań')
    plt.title('Ilość mieszkań w bazie danych w poszczególnych miastach')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.bar(df['city'], df['price'])
    
    plt.grid(True, axis='y', linestyle = ':', alpha=0.5)
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.show()

def num_in_date(df):
    plt.figure(figsize = (10,5))
    df = df.groupby(['date'])['price'].count().reset_index()
    df = df.sort_values(by = 'date')

    plt.xlabel('Data')
    plt.ylabel('Ilość mieszkań')
    plt.title('Ilość mieszkań w bazie danych w poszczególnych miesiącach')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.bar(df['date'], df['price'])
    
    plt.grid(True, axis='y', linestyle = ':', alpha=0.5)
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.show()

def scatter_plot_price_meters(df):

    plt.figure(figsize = (12,8))
    sns.scatterplot(data=df, x='squareMeters', y='price', alpha=0.3)
    sns.regplot(data=df, x='squareMeters', y='price', scatter=False, color='red', line_kws={"lw": 2})

    plt.title('Rozkład punktowy mieszkań')
    
    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation = 45)
 
    plt.tight_layout()
    plt.show()

def boxplot_city_price(df):

    df = df.sort_values(by = 'price', ascending = False)
    plt.figure(figsize=(12, 8))
    sns.boxplot(x = 'city', y='price', data = df, hue = 'city', palette = 'viridis', dodge = False)

    plt.xlabel('Miasto')
    plt.ylabel('Cena mieszkania (PLN)')
    plt.title('Rozkład cen mieszkań w zależności od miasta')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.grid(True, axis='y', linestyle = ':', alpha=0.5)
    plt.xticks(rotation = 45)

    plt.tight_layout()
    plt.show()

def boxplot_price_per_meter_sqared(df):

    df['price_per_sqm'] = df['price'] / df['squareMeters']
    plt.figure(figsize=(12, 8))
    sns.boxplot(x = 'city', y='price_per_sqm', data = df, hue = 'city', palette = 'viridis', dodge = False)

    plt.xlabel('Miasto')
    plt.ylabel('Cena metra kwadratowego (PLN)')
    plt.title('Rozkład cen metra kwadratowego w zależności od miasta')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.grid(True, axis='y', linestyle = ':', alpha=0.5)
    plt.xticks(rotation = 45)

    plt.tight_layout()
    plt.show()

def price_per_m2_compared_to_mean_salary(df):

    # sources: https://300gospodarka.pl/news/oto-mapa-polskich-plac-mamy-nowy-ranking-zarobkow-w-najwiekszych-miastach-grafika
    # https://zarobki.pracuj.pl/kalkulator-wynagrodzen/
    # dane na 04.2024 
    salary_map = {
        'warszawa': 7178,
        'krakow': 7591,
        'gdansk': 7284,
        'wroclaw': 6509,
        'poznan': 6186,
        'szczecin': 6040,
        'katowice': 6429,
        'bialystok': 4854,
        'rzeszow': 5979,
        'lublin': 5455,
        'lodz': 5567,
        'bydgoszcz': 5476
    }

    # source: https://bulldogjob.pl/it-report/2024/zarobki-w-it#general-zarobki-a-miasto-srednia_0
    # dane na 2024
    it_salary_map = {
        'warszawa': 9887,
        'krakow': 10009,
        'gdansk': 8486,
        'gdynia': 8486,
        'wroclaw': 9371,
        'poznan': 8591,
        'szczecin': 8206,
        'czestochowa': 7977,
        'katowice': 8293,
        'bialystok': 4854,
        'rzeszow': 5793,
        'lublin': 6976,
        'lodz': 8997,
        'bydgoszcz': 8852,
    }

    df['price_per_sqm'] = df['price'] / df['squareMeters']
    df = df.groupby(['city'])['price_per_sqm'].mean().reset_index()
    df['avg_salary'] = df['city'].map(salary_map)
    df['avg_it_salary'] = df['city'].map(it_salary_map)
    df['m2_per_salary'] = df['price_per_sqm'] / df['avg_salary']
    df['m2_per_it_salary'] = df['price_per_sqm'] / df['avg_it_salary']

    df = df.sort_values(by = 'm2_per_it_salary')
    df = df.dropna(subset = 'm2_per_it_salary')

    plt.figure(figsize=(12, 8))
    
    bar_width = 0.35
    index = np.arange(len(df))

    plt.bar(index, df['m2_per_salary'], bar_width, label='porównując z średnią pensją', color='skyblue')
    plt.bar(index + bar_width, df['m2_per_it_salary'], bar_width, label='porównując z średnią pensją w IT', color='orange')

    plt.xlabel('miasto')
    plt.title('Rozkład ile średnich pensji (na rękę) trzeba, aby kupic 1 metr kwadratowy')

    plt.grid(True, axis='y', linestyle = ':', alpha=0.5)
    plt.xticks(index + bar_width / 2, df['city'], rotation = 45)

    plt.tight_layout()
    plt.legend()
    plt.show()

def hist_building_material_build_year(df):

    plt.figure(figsize=(15,5))
    plt.title("Materiał budowy, a data budowy")
    plt.hist(df[df['buildingMaterial'] == 'brick']['buildYear'], bins=20, label="Cegła")
    plt.hist(df[df['buildingMaterial'] == 'concreteSlab']['buildYear'], bins=20, label="Płyta betonowa")
    
    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))
    
    plt.legend()
    plt.tight_layout()
    plt.show()

def hist_type_build_year(df):

    plt.figure(figsize=(15,5))
    plt.title("Typ budynku, a data budowy")
    plt.hist(df[df['type'] == 'blockOfFlats']['buildYear'], bins=20, label="blok mieszkalny")
    plt.hist(df[df['type'] == 'apartmentBuilding']['buildYear'], bins=20, label="apartmentowiec")
    plt.hist(df[df['type'] == 'tenement']['buildYear'], bins=20, label="kamienica")
    
    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))
    
    plt.legend()
    plt.tight_layout()
    plt.show()

def hist_size(df):

    plt.figure(figsize=(10,3))
    plt.title("Rozmiar mieszkania")
    plt.hist(df['squareMeters'], bins=20)
    
    plt.tight_layout()
    plt.show()

def floor_data(df):

    plt.figure(figsize = (8,8))

    df = df.groupby(['floor', 'floorCount'])['price'].count().reset_index()
    df = df.sort_values(by = 'floor', ascending = True)

    plt.xlabel('Ilość pięter budynku')
    plt.ylabel('Piętro mieszkania')
    plt.scatter(df['floorCount'], df['floor'], c=df['price'], cmap='coolwarm', s=80, marker='s')
    plt.show()

def features_stats(df):

    def get_feature_stats(feature):
        featureStats = pd.DataFrame(df[df[feature] == 1].groupby(['city'])[feature].count()).reset_index()
        featureStats['all'] = pd.DataFrame(df.groupby(['city'])['price'].count()).reset_index().rename({'price': 'all'}, axis=1)['all']
        featureStats['percentage'] = featureStats[feature] / featureStats['all']
        return featureStats.sort_values(['percentage'], ascending=True)

    features = ['hasParkingSpace', 'hasBalcony', 'hasElevator', 'hasSecurity', 'hasStorageRoom']
    fig = plt.figure(figsize = (13, 8))
    i = 0
    for feature in features:
        i += 1
        subplot = fig.add_subplot(2,3,i)
        stats = get_feature_stats(feature)
        subplot.set_title(feature)
        subplot.barh(stats['city'], stats['percentage'], color = 'skyblue')
        subplot.set_xlim(0,1)
        subplot.xaxis.set_major_formatter(tick.PercentFormatter(1))
        subplot.grid(True, axis = 'x', linestyle = ':', alpha = 0.5)

    
    plt.subplots_adjust(wspace = 0.8)
    plt.tight_layout()
    plt.show()

def avg_cost_with_and_without_features(df):
    
    features = ['hasParkingSpace', 'hasBalcony', 'hasElevator', 'hasSecurity', 'hasStorageRoom']
    fig = plt.figure(figsize = (10, 6))
    i = 0
    handles = []
    labels = []

    for feature in features:
        i += 1
        subplot = fig.add_subplot(2,3,i)
        stats = df.groupby(feature)['price'].agg(
            mean_price = 'mean',
            median_price = 'median'
        ).reset_index()

        bar_width = 0.4
        x = stats[feature]
        mean_bar = subplot.bar(x - bar_width / 2, stats['mean_price'], bar_width,
                     label = 'Średnia', color = 'skyblue')
        median_bar = subplot.bar(x + bar_width / 2, stats['median_price'], bar_width,
                     label = 'Mediana', color = 'orange')
    
        if i == 1:
            handles.extend([mean_bar, median_bar])
            labels.extend(['Średnia', 'Mediana'])

        subplot.set_title(feature)
        subplot.set_xlim(-0.5, 1.5)
        subplot.set_xticks([0, 1])
        subplot.set_xticklabels(['no', 'yes'])
        subplot.grid(True, axis = 'y', linestyle = ':', alpha = 0.5)
    
    plt.subplots_adjust(wspace = 0.8)
    plt.tight_layout()
    plt.legend(handles, labels, loc = 'lower right', bbox_to_anchor = (2.2, 0.3), ncol = 2)
    plt.show()

def history_of_prices(df):
    
    df_mean = df.groupby('date')['price'].mean().reset_index()
    df_median = df.groupby('date')['price'].median().reset_index()

    plt.figure(figsize=(10, 5))
    plt.plot(df_mean['date'], df_mean['price'], marker='o', label='Średnia')
    plt.plot(df_median['date'], df_median['price'], marker='o', label='Mediana', linestyle='--')

    plt.xlabel('Data')
    plt.ylabel('Cena mieszkań')
    plt.title('Zmiana ceny mieszkań w czasie')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.grid(True, axis='y', linestyle='--', alpha=0.5)

    plt.legend()
    plt.tight_layout()
    plt.show()

def dist_from_centre_cost(df):

    df['distance_group'] = pd.cut(df['centreDistance'], bins = 15)
    df['mid_point'] = df['distance_group'].apply(lambda x: round(x.mid, 1))
    df = df.groupby('mid_point')['price'].mean().reset_index()

    plt.figure(figsize = (12,6))
    plt.plot(df['mid_point'], df['price'], marker = 'o')
    
    plt.xlabel('Odległość od centrum (km)')
    plt.ylabel('Cena mieszkań')
    plt.title('Zmiana ceny mieszkań w zależności od odległości od centrum')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation = 45)
 
    plt.tight_layout()
    plt.show()

def dist_from_centre_m2_cost(df):

    df['price_per_m2'] = df['price']/df['squareMeters']
    df['distance_group'] = pd.cut(df['centreDistance'], bins = 15)
    df['mid_point'] = df['distance_group'].apply(lambda x: round(x.mid, 1))
    df = df.groupby('mid_point')['price_per_m2'].mean().reset_index()

    plt.figure(figsize = (12,6))
    plt.plot(df['mid_point'], df['price_per_m2'], marker = 'o')
    
    plt.xlabel('Odległość od centrum (km)')
    plt.ylabel('Cena metra kwadratowego')
    plt.title('Zmiana ceny metra kwadratowego w zależności od odległości od centrum')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation = 45)
 
    plt.tight_layout()
    plt.show()

def meters_dist_from_centre(df):
    df['distance_group'] = pd.cut(df['centreDistance'], bins = 15)
    df['mid_point'] = df['distance_group'].apply(lambda x: round(x.mid, 1))
    df = df.groupby('mid_point')['squareMeters'].mean().reset_index()

    plt.figure(figsize = (12,6))
    plt.plot(df['mid_point'], df['squareMeters'], marker = 'o')
    
    plt.xlabel('Odległość od centrum (km)')
    plt.ylabel('Średni metraż mieszkań')
    plt.title('Wielkość mieszkań w zależności od odległości od centrum')

    plt.show()

def dist_from_school_cost(df):

    df['distance_group'] = pd.cut(df['schoolDistance'], bins = 10)
    df['mid_point'] = df['distance_group'].apply(lambda x: round(x.mid, 1))
    df = df.groupby('mid_point')['price'].mean().reset_index()

    plt.figure(figsize = (12,6))
    plt.plot(df['mid_point'], df['price'], marker = 'o')
    
    plt.xlabel('Odległość od szkoły (km)')
    plt.ylabel('Cena mieszkań')
    plt.title('Zmiana ceny mieszkań w zależności od odległości od szkoły')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation = 45)

    plt.tight_layout()
    plt.show()

def dist_from_college_cost(df):

    df['distance_group'] = pd.cut(df['collegeDistance'], bins = 10)
    df['mid_point'] = df['distance_group'].apply(lambda x: round(x.mid, 1))
    df = df.groupby('mid_point')['price'].mean().reset_index()

    plt.figure(figsize = (12,6))
    plt.plot(df['mid_point'], df['price'], marker = 'o')
    
    plt.xlabel('Odległość od szkoły wyższej (km)')
    plt.ylabel('Cena mieszkań')
    plt.title('Zmiana ceny mieszkań w zależności od odległości od szkoły wyższej')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation = 45)

    plt.tight_layout()
    plt.show()

def poi_count_dist_from_centre(df):
    df['distance_group'] = pd.cut(df['centreDistance'], bins = 15)
    df['mid_point'] = df['distance_group'].apply(lambda x: round(x.mid, 1))
    df = df.groupby('mid_point')['poiCount'].mean().reset_index()

    plt.figure(figsize = (12,6))
    plt.plot(df['mid_point'], df['poiCount'], marker = 'o')
    
    plt.xlabel('odległość od centrum (km)')
    plt.ylabel('ilość POI')
    plt.title('Ilość POI w zależności od odległości od centrum')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))

    plt.grid(True, axis='y', linestyle='--', alpha=0.5)
    plt.xticks(rotation = 45)
 
    plt.tight_layout()
    plt.show()

def correlation(df):

    type_price_avg = df.groupby('type')['price'].mean()
    type_sorted = type_price_avg.sort_values(ascending=True).index
    type_mapping = {type_: idx for idx, type_ in enumerate(type_sorted)}
    df['type_numerical'] = df['type'].map(type_mapping)
    
    city_price_avg = df.groupby('city')['price'].mean()
    city_sorted = city_price_avg.sort_values(ascending=True).index
    city_mapping = {city: idx for idx, city in enumerate(city_sorted)}
    df['city_numerical'] = df['city'].map(city_mapping)

    df['price_per_m2'] = df['price']/df['squareMeters']

    numeric_cols = ['price','price_per_m2', 'squareMeters',  'rooms', 'floor', 'floorCount', 'buildYear',
                'centreDistance', 'poiCount', 'schoolDistance', 'collegeDistance',
                'hasParkingSpace', 'hasBalcony', 'hasElevator', 'hasSecurity',
                'hasStorageRoom', 'type_numerical', 'city_numerical']

    correlation = df[numeric_cols].corr()

    plt.figure(figsize=(10, 10))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Macierz korelacji')

    plt.tight_layout()
    plt.show()


conn = sqlite3.connect('apartments.db')
query = "SELECT * FROM apartments_sale"
df = pd.read_sql_query(query, conn)
#df = df.drop_duplicates(subset='id', keep='last')
dist_from_college_cost(df)