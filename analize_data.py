import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

def boxplot_city_price(df):

    df_sorted = df.sort_values(by = 'price', ascending = False)
    plt.figure(figsize=(12, 8))
    sns.boxplot(x = 'city', y='price', data = df_sorted, hue = 'city', palette = 'viridis', dodge = False)

    plt.xlabel('Miasto')
    plt.ylabel('Cena mieszkania (PLN)')
    plt.title('Rozkład cen mieszkań w zależności od miasta')

    axis = plt.gca()
    axis.yaxis.set_major_formatter(tick.FuncFormatter(lambda x, _: f'{int(x):,}'.replace(',', ' ')))


    plt.grid(True, axis='y', linestyle = ':', alpha=0.5)
    plt.xticks(rotation = 45)

    plt.tight_layout()
    plt.show()
 

conn = sqlite3.connect('apartments.db')  
query = "SELECT * FROM apartments_sale"
df = pd.read_sql_query(query, conn)

boxplot_city_price(df)