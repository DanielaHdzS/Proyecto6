
# ! Proyecto 6

# ? Sprint 6


# TODO: Descripcion del proyecto
# *Trabajas para la tienda online Ice que vende videojuegos por todo el mundo. Las reseñas de usuarios y expertos, los géneros, las plataformas (por ejemplo, Xbox o PlayStation) y los datos históricos sobre las ventas de juegos están disponibles en fuentes abiertas. Tienes que identificar patrones que determinen si un juego tiene éxito o no. Esto te permitirá detectar proyectos prometedores y planificar campañas publicitarias.
# *Delante de ti hay datos que se remontan a 2016. Imaginemos que es diciembre de 2016 y estás planeando una campaña para 2017.
# *(Lo importante es adquirir experiencia de trabajo con datos. Realmente no importa si estás pronosticando las ventas de 2017 en función de los datos de 2016 o las ventas de 2027 en función de los datos de 2026.)
# *El dataset contiene la abreviatura ESRB. The Entertainment Software Rating Board (la Junta de clasificación de software de entretenimiento) evalúa el contenido de un juego y asigna una clasificación de edad como Adolescente o Adulto.


# ? Paso 1. Abre el archivo de datos y estudia la información general

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st


games = pd.read_csv(
    'https://raw.githubusercontent.com/DanielaHdzS/Proyecto6/main/games.csv')
print(games.head())


# ? Paso 2. Prepara los datos


games.columns = games.columns.str.lower()
print(games.head())


games.info()


games.isna().sum()


games['genre'] = games['genre'].dropna()
games['rating'] = games['rating'].dropna()
games['critic_score'] = games['critic_score'].dropna()
games['user_score'] = games['user_score'].dropna()
games['year_of_release'] = games['year_of_release'].dropna()


# * Sugiero que los datos estan ausentes ya que es posible:
# *1. Para el caso del genero, puede que los datos ausentes sean un tipo de genero que no tuvo gran relevancia como para colocarlo dentro de una categoria.
# *2. Para user_score y critic_score, puede que al momento de que los usuarios colocaban la calificacion, no lo ponian dentro del formato establecido o dentro del rango establecido, o no opinaban de ese juego ya que no lo conocian o no lo habian jugado.
# *3. En el caso de rating, puede suceder lo mismo que en el caso de genero, que exista un rating que no mucha gente voto y por eso no es considerado.
# *4. Para el caso de year_of_release, puede que al momento de colocar los años dentro de dataset se tuvieron errores en su año de registro de las consolas.


games['user_score'] = games['user_score'].replace('tbd', 11.0)
print(games['user_score'].unique())


# *Para poder trabajar con el tipo de dato float, considere cambiar tbd por un numero que estuviera fuera del rango para poder diferenciarlo del resto


games['year_of_release'] = games['year_of_release'].fillna(1979)

# *Los valores ausentes se rellenaron con valores en cero, el unico que no lo considere asi fue el de year_of_release, esto debido a que si lo pongo en cero, el dato estaria muy sesgado, lo cual haria que la informacion que se presente graficamente o visualmente estuviera muy limitada.


games['name'] = games['name'].astype(str)
games['platform'] = games['platform'].astype(str)
games['year_of_release'] = games['year_of_release'].astype(int)
games['genre'] = games['genre'].astype(str)
games['user_score'] = games['user_score'].astype(float)
games['rating'] = games['rating'].astype(str)


games['sum_total'] = games['na_sales'] + games['eu_sales'] + \
    games['jp_sales'] + games['other_sales']
print(games.head())


# ? Paso 3. Analiza los datos


games_year = games.groupby('year_of_release')['name'].count()
games_year = games_year.reset_index()
games_year = games_year.sort_values(by='name', ascending=False)
print(games_year)


# *Podemos ver que durante el 2008 fue el año en el que mas juegos se lanzaron.


list_sales = ['na_sales', 'eu_sales', 'jp_sales', 'other_sales', 'sum_total']
games_year = games.groupby('year_of_release')[list_sales].sum()
games_year = games_year.reset_index()
games_year = games_year.sort_values(by='sum_total', ascending=False)
print(games_year)


plt.hist(games_year['year_of_release'], bins=7,
         color='teal', edgecolor='black')
plt.xlabel('year_of_release')
plt.ylabel('Frecuencia')
plt.title('Histograma por Anios')
plt.show()


plt.figure(figsize=(4, 3))
sns.boxplot(x=games_year['sum_total'], width=0.6,
            showmeans=True, meanline=True, notch=True)
plt.xlabel('Suma total')
plt.title('Diagrama de Caja')
plt.show()


plt.bar(games_year['year_of_release'],
        games_year['sum_total'], color='teal', edgecolor='black')
plt.xlabel('Lanzamiento')
plt.ylabel('Suma Total')
plt.title('Grafico de barras por Anios')
plt.show()


# * Se realizo una agrupacion por años de las ventas totales que se obtuvieron en todas las regiones (na,eu,jp y otros), en la grafica de barras podemos ver que el incremento en las ventas empezo 2004 alcanzo su mayor punto en el 2008, de ahi fue bajando gradualmente.


games_platform = games.groupby('platform')[list_sales].sum()
games_platform = games_platform.reset_index(
).sort_values(by='sum_total', ascending=False)
print(games_platform)


plt.figure(figsize=(15, 5))
plt.hist(games_platform['platform'], bins=15,
         color='midnightblue', edgecolor='black')
plt.xlabel('platform')
plt.ylabel('Frecuencia')
plt.title('Histograma por Plataforma')
plt.show()


plt.figure(figsize=(6, 3))
sns.boxplot(x=games_platform['sum_total'], width=0.6)
plt.xlabel('Suma total')
plt.title('Diagrama de Caja')
plt.show()


plt.figure(figsize=(15, 5))
plt.bar(games_platform['platform'], games_platform['sum_total'],
        color='midnightblue', edgecolor='black')
plt.xlabel('Plataforma')
plt.ylabel('Suma Total')
plt.title('Grafico de barras de las ventas por plataforma')
plt.show()


# *La consola PS2 fue la que mas ventas tuvo a comparacion de las demas.


games_year_platform = games.groupby(['year_of_release', 'platform'])[
    list_sales].sum()
games_year_platform = games_year_platform.reset_index()
print(games_year_platform)


games_handhelds = games_year_platform.query("year_of_release >= 2013")[
    ['year_of_release', 'platform', 'sum_total']]
print(games_handhelds.sort_values(by='sum_total', ascending=False))


# *Se hace un filtrado donde escogemos del año 2013 en adelante para visualizar que consolas son las que han tenido mayor venta en los ultimos 5 años


plt.figure(figsize=(15, 5))
plt.bar(games_handhelds['platform'], games_handhelds['sum_total'],
        color='midnightblue', edgecolor='black')
plt.xlabel('Plataforma')
plt.ylabel('Suma Total')
plt.title('Grafico de barras de las ventas por plataforma')
plt.show()


plt.figure(figsize=(10, 6))
sns.scatterplot(x='year_of_release', y='sum_total',
                hue='platform', data=games_handhelds, s=100)
plt.xticks(range(2013, 2017))
plt.xlabel('Año de lanzamiento')
plt.ylabel('Suma total')
plt.legend(title='Plataforma')
plt.title('Gráfico de Dispersión con Tres Variables')
plt.show()


# *En el gráfico anterior podemos interpretar la información:
# *1. Las consolas de Sony PS4 y PS3 fueron las que mas ventas tuvieron y que estuvieron dentro de un rango de ventas similar durante estos ultimos años, sin embargo, la PS3 decayo en ventas despues del 2013.
# *2. La consola de Microsoft, la Xbox One fue la segunda con mas ventas durante estos años, la consola X360 tuvo buenas ventas en el año 2013 pero fue decayendo durante los proximos años, esto puede deberse, que al igual que su competencia la PS3, empezaron a quedarse atras por el lanzamiento de las nuevas consolas de cada compañia .
# *3.  Mientras que las consolas de Nintendo fueron en general las que menos ventas tuvieron, pero todas las consolas DS, Wii, WiiU se mantuvieron en cuanto a ventas.
#
# *De esto, podemos decir que Sony es la compañia que mas vende en cuanto a juegos por plataforma, a pesar de tener rivalidad con las consolas que ofrece Microsoft, el target de estas dos consolas en general es el mismo, mientras que el target de Nintendo es diferente, tal vez podria ser esta la razon del porque las ventas de Nintendo son menores a sus competidores.
#
# *Para seguir con el analisis, escogere la consola de cada plataforma que tuvo mas ventas durante estos años, las cuales sera: PS4, PS3, X360 y XOne.


list_platform = ['PS4', 'XOne', 'PS3', 'X360']
games_name = games.query(
    "platform  in @list_platform")[['name', 'platform', 'sum_total']]
games_name = games_name.sort_values(by='sum_total', ascending=False)
print(games_name)


plt.figure(figsize=(8, 6))
sns.boxplot(x=games_name['platform'], y=games_name['sum_total'], color='skyblue', width=0.6, showmeans=True,
            meanline=True, notch=True, flierprops=dict(markerfacecolor='mediumturquoise', marker='D'))
plt.xlabel('Plataforma')
plt.ylabel('Suma total')
plt.title('Diagrama de Caja')
plt.show()


# *En el diagrama de cajas anterior, podemos ver que los valores atipicos son los que predominan en las 4 consolas.


plt.figure(figsize=(8, 6))
sns.boxplot(x=games_name['platform'], y=games_name['sum_total'], color='skyblue', width=0.6, showmeans=True,
            showfliers=False, meanline=True, notch=True, flierprops=dict(markerfacecolor='mediumturquoise', marker='D'))
plt.xlabel('Plataforma')
plt.ylabel('Suma total')
plt.title('Diagrama de Caja')
plt.show()


# *En este otro diagrama de cajas, quitamos los valores atipicos para poder ver con mayor exactitud la informacion de cada consola.
# *1. Nos muestra que el primer cuartil esta casi igual para las consolas X360 y PS3, y casi igual para las otras dos consolas.
# *2. Con el segundo cuarti pasa lo mismo, donde tenemos las consolas X360 y PS3 iguales y las consolas PS4 y XOne ligeramente similares.
# *3. El tercer cuartil, se nota la diferencia entre consolas, donde X360 y PS3 tienen similud pero PS4 esta mas arriba que la XOne.
# *4. La linea discontinua nos muestra la media, la cual es si varia entre cada consola, mientras que la del PS4 y X360 esta por arriba del tercer cuartil, la del XOne y PS3 se mantiene un poco por debajo del tercer cuartil.
#
#
# *Para analizar los juegos de cada plataforma, se escogeran los primeros 5 juegos con mayores ventas y que tengan relacion alguna con las plataformas.


games_name_ps4 = games_name.query("platform  == 'PS4'")[
    ['name', 'platform', 'sum_total']]
games_name_ps4 = games_name_ps4.sort_values(by='sum_total', ascending=False)
print(games_name_ps4.head())


top_ps4 = games_name_ps4.head(5)
plt.figure(figsize=(15, 6))
plt.bar(top_ps4['name'], top_ps4['sum_total'],
        color='goldenrod', edgecolor='black')
plt.xlabel('Videojuego')
plt.ylabel('Suma Total')
plt.title('Top 5 juegos mas vendidos para la PS4')
plt.show()


games_name_xone = games_name.query("platform  == 'XOne'")[
    ['name', 'platform', 'sum_total']]
games_name_xone = games_name_xone.sort_values(by='sum_total', ascending=False)
print(games_name_xone)


top_xone = games_name_xone.head(5)
plt.figure(figsize=(15, 6))
plt.bar(top_xone['name'], top_xone['sum_total'],
        color='darkmagenta', edgecolor='black')
plt.xlabel('Videojuego')
plt.ylabel('Suma Total')
plt.title('Top 5 juegos mas vendidos para la XOne')
plt.show()


games_name_x360 = games_name.query("platform  == 'X360'")[
    ['name', 'platform', 'sum_total']]
games_name_x360 = games_name_x360.sort_values(by='sum_total', ascending=False)
print(games_name_x360)


top_x360 = games_name_x360.head(5)
plt.figure(figsize=(15, 6))
plt.bar(top_x360['name'], top_x360['sum_total'],
        color='steelblue', edgecolor='black')
plt.xlabel('Videojuego')
plt.ylabel('Suma Total')
plt.title('Top 5 juegos mas vendidos para la X360')
plt.show()


games_name_ps3 = games_name.query("platform  == 'PS3'")[
    ['name', 'platform', 'sum_total']]
games_name_ps3 = games_name_ps3.sort_values(by='sum_total', ascending=False)
print(games_name_ps3)


top_ps3 = games_name_ps3.head(5)
plt.figure(figsize=(15, 6))
plt.bar(top_ps3['name'], top_ps3['sum_total'],
        color='slategray', edgecolor='black')
plt.xlabel('Videojuego')
plt.ylabel('Suma Total')
plt.title('Top 5 juegos mas vendidos para la PS3')
plt.show()


# *Analizamos la consola PS4 ya que fue la que mas ventas tuvo en comparacion con las otras 3. Para poder verificar si existe relacion alguna entre las criticas de los usuarios o de los profesionales en relacion con las ventas.


games_score = games.query("platform == 'PS4'")[
    ['name', 'critic_score', 'user_score', 'sum_total']]
games_score = games_score.sort_values(by='sum_total', ascending=False)
print(games_score)
print(games_score.describe())


plt.figure(figsize=(8, 6))
sns.scatterplot(x='critic_score', y='user_score', hue='sum_total',
                data=games_score, palette='rocket', sizes=(50, 200))
plt.xlabel('Reseña Profesional')
plt.ylabel('Reseña Usuario')
plt.title('Diagrama de Dispersion')
plt.show()


games_score_corr = games.query("platform == 'PS4'")[
    ['critic_score', 'user_score', 'sum_total']]
games_score_corr = games_score_corr.sort_values(
    by='sum_total', ascending=False)
matriz_correlacion = games_score_corr.corr()
print(matriz_correlacion)


# *Podemos ver que la correlacion entre la critica profesional y las ventas es de 0.4, casi cero por lo que indica una relacion positiva casi lineal.
# *La relacion entre la critica de los usuarios y las ventas da un valor negativo -0.063 aproximado a cero, lo que indica una correlacion negativa, por lo que mientras una aumenta la otra tiende a disminuir.
#
# *De hecho, podemos ver por ejemplo, COD BO3 no tiene criticas ni profesional ni de los usuarios, y aun asi fue de los juegos mas vendidos en las 4 consolas que estamos analizando.


games_name_ps4.head()


games_list = ['Call of Duty: Black Ops 3', 'Grand Theft Auto V', 'FIFA 16',
              'Star Wars Battlefront (2015)', 'Call of Duty: Advanced Warfare']
games_top_xone = games_name_xone.query(
    'name in @games_list')[['name', 'sum_total']]
print(games_top_xone)


games_top_x360 = games_name_x360.query(
    'name in @games_list')[['name', 'sum_total']]
print(games_top_x360)


games_top_ps3 = games_name_ps3.query(
    'name in @games_list')[['name', 'sum_total']]
print(games_top_ps3)


# *Comparando las ventas del top 5 juegos mas vendidos por la consola PS4, donde el top de juegos son:
# *1. Call of Duty: Black Ops
# *2. Grand Theft Auto V
# *3. Star Wars Battlefront
# *4. FIFA 16
# *5.Call of Duty: Advanced Warfare
#
# *Se concluye que:
# *1. COD: BO3 se tiene en las 4 consolas donde en la consola PS4 se tuvieron mayores ventas y en la PS3 donde se tuvo las menores ventas de este videojuego.
# *2. El GTA V es el juego que comparten en el top las 4 consolas, donde en la PS3 se tuvo las mayores ventas y en el XOne las menores ventas, sin embargo, es el juego mas vendido entre las 4 consolas.
# *3. Star Wars Battlefront solo la tienen la consola PS4 y XOne, donde la consola XOne tuvo las menores ventas.
# *4. FIFA 16 fue el mas vendido en la consola PS4.
# *5. COD: Advanced Warfare fue el mas vendido en el X360.


games_genre = games.groupby(['platform', 'genre'])['sum_total'].sum()
games_genre = games_genre.reset_index()
print(games_genre)


plt.figure(figsize=(15, 5))
sns.scatterplot(x='genre', y='sum_total',  data=games_genre, sizes=(50, 200))
plt.xlabel('Genero')
plt.ylabel('Ventas Totales')
plt.title('Diagrama de Dispersion del Genero y Ventas Totales')
plt.show()

# *En el grafico de Genero y Ventas, podemos ver que el genero mas rentable es de Action, junto con Sports y Shooter, mientras que los menos rentables son Strategy, Adventure y Puzzle.
#
# *Si vemos el top 5 de juegos mas vendidos, vemos que el juego COD:BO3 es del genero Shooter.


# ? Paso 4. Crea un perfil de usuario para cada región


agg_region = {'na_sales': 'sum', 'eu_sales': 'sum', 'jp_sales': 'sum'}
genre_region = games.groupby(['genre'])
genre_region = genre_region.agg(agg_region)
print(genre_region.sort_values(by='na_sales', ascending=False).head(5))
print(genre_region.sort_values(by='eu_sales', ascending=False).head(5))
print(genre_region.sort_values(by='jp_sales', ascending=False).head(5))


# *Podemos ver que cada tabla nos muestra que genero fue el más vendido en esa región.
# *Para la region de NorteAmerica, el genero Action fue el mas vendido mientras que en la región de Japón este genero fue el de menor ventas.
# *Para la región de Europa, tambien fue el genero de Action el que tuvo mayores ventas y de igual forma en Japón fue donde menor venta tuvo.
# *Para la región de Japón, el que tuvo mayores ventas fue el Role-Playing, para este genero la region de Europa fue donde menor venta hubo.


genre_region = games.groupby(['platform'])
genre_region = genre_region.agg(agg_region)
print(genre_region.sort_values(by='na_sales', ascending=False).head(5))
print(genre_region.sort_values(by='eu_sales', ascending=False).head(5))
print(genre_region.sort_values(by='jp_sales', ascending=False).head(5))


# *En cuanto a plataforma, en la región de NA la plataforma con mayores ventas fue el X360, y donde hubo menor venta fue en la region de JP.
# *En la región de EU fue la plataforma PS2 la que tuvo mayores ventas, de igual forma, JP fue donde hubo menor venta.
# *Para la región JP, la consola DS tuvo mayores ventas y en la región EU fue donde menor venta tuvo esta plataforma.


genre_region = games.groupby(['rating'])
genre_region = genre_region.agg(agg_region)
print(genre_region.sort_values(by='na_sales', ascending=False).head(5))
print(genre_region.sort_values(by='eu_sales', ascending=False).head(5))
print(genre_region.sort_values(by='jp_sales', ascending=False).head(5))


# *Para el rating, tenemos valores NaN los cuales sesgan nuestro analasis, no se tomaran en cuenta, asi que la clasificacion E, que es la que es apta para toddo publico, es la que tuvo mayores ventas en las 3 regiones.


# *En general, viendo los datos por region, el rating no afecta directamente a la venta de los juegos. Las 3 regiones comparten varios generos con ventas que difieren bastante de una region a otra. Tambien podemos observar que el tipo de consola que tiene mayor venta de videojuegos es diferente, mientras que en NA es la consola creada por Microsoft, una empresa que tiene sus raices dentro del mercado norteamericano. Despues, la region de EU, donde la consola de Sony es la que mayores ventas tiene y donde Sony ha enfocado mas su mercadotecnia, por ultimo, la consola de Nintendo, una empresa creada en Japon y donde se concentra la mayoria de sus ventas.


# ? Paso 5. Prueba las siguientes hipótesis:
# *1. Las calificaciones promedio de los usuarios para las plataformas Xbox One y PC son las mismas.
#


list_platform = ['XOne', 'PC']
platform_score = games.query(
    'platform in @list_platform & user_score != 11.0')[['platform', 'user_score']]
platform_score = platform_score.dropna()
print(platform_score)


xone_score = platform_score.query('platform == "XOne"')[['user_score']]
print(xone_score)


pc_score = platform_score.query('platform == "PC"')[['user_score']]
print(pc_score)


print(xone_score.var())
print(pc_score.var())


alpha = 0.05
results = st.ttest_ind(xone_score, pc_score, equal_var=True)

print('valor p: ', results.pvalue)
if results.pvalue < alpha:
    print("Rechazamos la hipótesis nula")
else:
    print("No podemos rechazar la hipótesis nula")


# *Nuestra hipotesis se basa en que las medias de dos poblaciones independientes son iguales.
# * Utilizamos los datos de los datasets filtrados para las plataformas XOne y PC, considere el valor de equal_var en True, ya que las varianzas son aproximadamente iguales. Aplicamos el analisis estadistico, hipotesis sobre la igualdad de las medias de dos poblaciones.
# *El valor de p esta por debajo del valor de alpha, esto sugiere que los datos que se proporcionan son suficientes para decir que hay una diferencia significativa entre las dos poblaciones,por lo que rechazamos la hipotesis nula.


# * ### 2. Las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes.


list_genre = ['Action', 'Sports']
genre_score = games.query(
    'genre in @list_genre and user_score != 11.0')[['genre', 'user_score']]
genre_score = genre_score.dropna()
print(genre_score)


action_score = genre_score.query('genre == "Action"')[['user_score']]
print(action_score)


sports_score = genre_score.query('genre == "Sports"')[['user_score']]
print(sports_score)


print(action_score.var())
print(sports_score.var())


alpha = 0.05
results = st.ttest_ind(action_score, sports_score, equal_var=False)
print('valor p: ', results.pvalue)
if results.pvalue < alpha:
    print("Rechazamos la hipótesis nula")
else:
    print("No podemos rechazar la hipótesis nula")


# *Nuestra hipotesis se basa en que las medias de dos poblaciones independientes son iguales.
# *Utilizamos los datos de los datasets filtrados para las plataformas XOne y PC. Aplicamos el analisis estadistico hipotesis sobre la igualdad de las medias de dos poblaciones, coloque el valor de equal_var = False, ya que considero que la varianza entre las dos poblaciones es significativa hipotesis sobre la igualdad de las medias de dos poblaciones.
# *El valor de p esta por arriba del valor de alpha, por lo que no podemos rechazar la hipotesis nula, por lo que no hay suficiente evidencia para afirmar que hay una gran diferencia entre las dos poblaciones.


# ? ### Paso 6. Escribe una conclusión general


# ! En conclusión:
# *1. Siempre al inicio de un proyecto se deben estudiar los datos, investigar sobre de que trata el proyecto y tener conocimiento del tema que se esta analizando, para esto se debe hacer la limpieza de datos, examinar columnas o filas que puedan contener valores nulos o valos atipicos, por ejemplo, se tiene el caso en que para la consola DS el año de lanzamiento aparecia en 1985, esto no es posible ya que se lanzo en los años 2000, si la persona que esta trabajando con los datos no conociera esta informacion, ya se tendria parte de la informacion erronea.
# *2. Cada region es diferente, para la region de NA la consola que mas vende es la de Microsoft, y los generos suelen ser de accion, deporte o shooter. En los generos, se comparte mucho con la region de EU, solo que la consola con mas ventas es la de Sony, mientra que la region JP, la consola y la empresa que mas vende es Nintendo. Con esta pequeña informacion, podemos ver que el target NA esta controlado por Microsoft, es posible que a diferencia de Sony, Microsoft aplique ciertas promociones o un marketing mas destacado. Sin embargo, tanto Sony como Microsoft no han logrado controlar el mercado de la region JP, donde Nintendo tiene gran ventaja, al igual, el genero que predomina suele ser mas tipos de juegos que puedes pasar tiempo con familiares o amigos, mientras que el target de Microsoft o Sony suele ser mas juegos en linea.
# *3. Para la parte de las pruebas de hipotesis, las pruebas arrojan que para las consolas XOne y PC, debemos rechazar la hipotesis nula, la cual nos dice que las calificaciones promedio de los usuarios son las mismas, pero para el caso de la segunda hipotesis nula donde el promedio de las calificaciones de los generos de accion y deportes son diferente, para este caso, no rechazamos esta hipotesis, lo cual implica que en efecto podemos decir que el promedio es diferente.
#
#
# todo: Asi mismo, hice este proyecto y lo subi a mi repositorio de Github para poder empezar a trabajar mas dentro de Git y estar mas familiarizada con este entorno, ya que estuve trabajando desde mi PC y luego utilizaba mi laptop. Dejo el link del repositorio: https://github.com/DanielaHdzS/Proyecto6.git
