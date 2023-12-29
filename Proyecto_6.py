import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

games = pd.read_csv('D:/Python/Tripleten/Proyectos/Sprint6/games.csv')
print(games.head())


games.columns = games.columns.str.lower()
print(games.head())


games.info()


games['user_score'].unique()


games['user_score'] = games['user_score'].replace('tbd', 11)


games['year_of_release'] = games['year_of_release'].fillna(1979)
games['user_score'] = games['user_score'].fillna(0)
games['rating'] = games['rating'].fillna(0)
games['critic_score'] = games['critic_score'].fillna(0)


games['name'] = games['name'].astype(str)
games['platform'] = games['platform'].astype(str)
games['year_of_release'] = games['year_of_release'].astype(int)
games['genre'] = games['genre'].astype(str)
games['user_score'] = games['user_score'].astype(float)
games['rating'] = games['rating'].astype(str)

games['sum_total'] = games['na_sales'] + games['eu_sales'] + \
    games['jp_sales'] + games['other_sales']
print(games.head())


list_sales = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales', 'sum_total']
games_year = games.groupby('year_of_release')[list_sales].sum()
games_year = games_year.reset_index()


games_year = games_year.sort_values(by='sum_total', ascending=False)


plt.hist(games_year['year_of_release'], bins=7,
         color='teal', edgecolor='black')
plt.xlabel('year_of_release')
plt.ylabel('Frecuencia')
plt.title('Histograma por Anios')
plt.show()

plt.bar(games_year['year_of_release'],
        games_year['sum_total'], color='teal', edgecolor='black')
plt.xlabel('Lanzamiento')
plt.ylabel('Suma Total')
plt.title('Grafico de barras por Anios')
plt.show()

games_platform = games.groupby('platform')[list_sales].sum()
games_platform = games_platform.reset_index()


games_platform = games_platform.sort_values(by='sum_total', ascending=False)
print(games_platform.head(10))


games_platform_10 = games_platform.head(10)
plt.hist(games_platform_10['platform'], bins=7,
         color='midnightblue', edgecolor='black')
plt.xlabel('platform')
plt.ylabel('Frecuencia')
plt.title('Histograma por Plataforma')
plt.show()


plt.bar(games_platform_10['platform'], games_platform_10['sum_total'],
        color='midnightblue', edgecolor='black')
plt.xlabel('Plataforma')
plt.ylabel('Suma Total')
plt.title('Grafico de barras de las ventas por plataforma')
plt.show()


games_year_platform = games.groupby(['year_of_release', 'platform'])[
    list_sales].sum()
print(games_year_platform)


print(games.query("platform == 'PS2' and year_of_release == 2008").head())
