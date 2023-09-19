import pandas as pd
from fastapi import FastAPI

#FastAPI
app = FastAPI()

#Carga de los datos
# Cargar los archivos para la primera funcion
df_first_function_file_one = pd.read_csv('03_datasets_proyecto_01/first_function_file_one.csv')
df_first_function_file_two = pd.read_csv('03_datasets_proyecto_01/first_function_file_two.csv')

#Cargar los archivos para la segunda funcion
df_second_function = pd.read_csv('03_datasets_proyecto_01/second_function_file_one.csv')

# Cargar los archivos para la tercera funcion
df_third_function = pd.read_csv('03_datasets_proyecto_01/third_function_file_one.csv')

# Cargar los archivos para la cuarta funcion
df_fourth_function = pd.read_csv('03_datasets_proyecto_01/fourth_function_file_one.csv')

# Cargar los archivos para la quinta funcion
df_fifth_function = pd.read_csv('03_datasets_proyecto_01/fifth_function_file_one.csv')

# Cargar los archivos para la sexta funcion
df_sixth_function = pd.read_csv('03_datasets_proyecto_01/sixth_function_file_one.csv')

#First_function: def userdata( User_id : str ): Debe devolver cantidad de dinero gastado por el usuario, 
#                el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

@app.get('/userdata/{user_id}')
def userdata(user_id:str):
    # Busca el 'user_id' en el DataFrame
    filter_df_first_function_file_one = df_first_function_file_one[df_first_function_file_one['user_id'] == user_id]
    # Si no se encuentra el 'user_id', devuelve None
    if filter_df_first_function_file_one.empty:
        return None, None
    # Si se encuentra el 'user_id', obtiene los valores de 'items_count' y 'price_float_column'
    items_count = filter_df_first_function_file_one.iloc[0]['items_count']
    price_float_column = filter_df_first_function_file_one.iloc[0]['price_float_column']
    price_float_column = round(price_float_column, 2)

    filter_recommend = df_first_function_file_two[df_first_function_file_two['user_id'] == user_id]
    if filter_recommend.empty:
        return None
    porcentaje_recommend = filter_recommend.iloc[0]['porcentaje_recommend']
    
    return {'spent_Money': price_float_column, 'items_count': items_count, 'percentage_recommend': porcentaje_recommend}

#Second function: def countreviews( YYYY-MM-DD y YYYY-MM-DD : str ): Cantidad de usuarios que realizaron 
#                 reviews entre las fechas dadas y, el porcentaje de recomendación de los mismos en base a reviews.recommend.

@app.get('/countreviews/{start_date}/{final_date}')
def countreviews (start_date:str, final_date:str):
    # Convierte la columna de fecha en tipo datetime
    df_second_function['new_date_format'] = pd.to_datetime(df_second_function['new_date_format'])
    # Define el rango de fechas deseado
    start_date_format = pd.to_datetime(start_date)
    final_date_format = pd.to_datetime(final_date)
    # Filtra el DataFrame para obtener las filas dentro del rango de fechas
    df_second_function_filter = df_second_function[(df_second_function['new_date_format'] >= start_date_format) & (df_second_function['new_date_format'] <= final_date_format)]
    # Realiza un conteo de valores únicos en otra columna (por ejemplo, 'otra_columna')
    count_user_id = df_second_function_filter['user_id'].nunique()

    count_total = df_second_function_filter['recommend'].count()
    filter_true = df_second_function_filter['recommend'] == True
    row_filters_review_true = df_second_function_filter[filter_true]
    count_total_true = row_filters_review_true['recommend'].count()
    percentage_recommend = (count_total_true/count_total)*100
    percentage_recommend = round(percentage_recommend, 2)

    # Imprime el conteo de valores únicos
    return {'count_user_review':count_user_id, 'percentage recommend': percentage_recommend}

# #Third Function: def genre( género : str ): Devuelve el puesto en el que se encuentra un género
# #               sobre el ranking de los mismos analizado bajo la columna PlayTimeForever.

@app.get('/genre/{genres}')
def genre (genres:str):
    # Utiliza explode() para convertir las listas en filas individuales
    filter_third_function = df_third_function[df_third_function['genres'] == genres]
    game_ranking = filter_third_function['ranking'].values[0]
    return {'game_ranking': game_ranking}

# # Fourth Function: def userforgenre( género : str ): Top 5 de usuarios con más horas de juego en el género dado, 
# #                  con su URL (del user) y user_id.

@app.get('/userforgenre/{genre}')
def userforgenre(genre:str):
# Filtra por el género deseado
    filtered_df = df_fourth_function[df_fourth_function['genres'] == genre]

    # Ordena el DataFrame filtrado por 'playtime_forever' en orden descendente
    sorted_df = filtered_df.sort_values(by='playtime_forever', ascending=False)

    # Toma los primeros 5 usuarios y almacénalos en una lista
    top_5_users_list = sorted_df.head(5)['user_id'].tolist()
    top_5_users_url_list = sorted_df.head(5)['user_url'].tolist()

    return {'user_id': top_5_users_list, 'user_url': top_5_users_url_list}

# # Fifth_Function: def developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free por año
# #                                según empresa desarrolladora. Ejemplo de salida:

@app.get('/developer/{developer_parameter}')
def developer(developer_parameter:str):
    df_developer = df_fifth_function.copy()
# Filtra el DataFrame por la desarrolladora especificada
    df_developer = df_developer[df_developer['developer'] == developer_parameter]

    # Convierte la columna "release_date" a tipo datetime para extraer el año
    df_developer['release_date'] = pd.to_datetime(df_developer['release_date'])
    df_developer['year'] = df_developer['release_date'].dt.year

    # Agrupa por año y calcula la cantidad de filas en la columna "price"
    grouped = df_developer.groupby('year')
    count_per_year = grouped['price'].count().reset_index()

    # Filtra las filas donde "price" es igual a "Free To Play"
    free_to_play_df = df_developer[df_developer['price'] == 'Free To Play']

    # Agrupa las filas de "Free To Play" por año y calcula la cantidad
    grouped_free_to_play = free_to_play_df.groupby('year')
    count_free_to_play_per_year = grouped_free_to_play['price'].count().reset_index()

    # Combina las dos tablas en una sola que contenga el recuento total y el recuento de "Free To Play" por año
    result = pd.merge(count_per_year, count_free_to_play_per_year, on='year', how='left')

    # Renombra las columnas para mayor claridad
    result.rename(columns={'price_x': 'total', 'price_y': 'free_to_play'}, inplace=True)
    result['free_to_play'] = result['free_to_play'].fillna(0)

    # Calcula el porcentaje de "Free To Play" en relación al total
    result['porcentaje_free_to_play'] = (result['free_to_play'] / result['total']) * 100

    data_dict = result.set_index('year')[['total', 'porcentaje_free_to_play']].to_dict(orient='index')

    # Transforma los valores en listas
    for year, values in data_dict.items():
        data_dict[year] = [values['total'], values['porcentaje_free_to_play']]

    # Imprime el diccionario resultante
    return data_dict

# # Sixth_Function: def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista
#                   con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con
#                   un análisis de sentimiento.

@app.get('/sentiment_analysis/{year}')
def sentiment_analysis(year:int):
    # Filtrar por el año deseado
    df_filtrado = df_sixth_function[df_sixth_function['year'] == year]
    
    negative = df_filtrado[df_filtrado['review'] == 0].shape[0]
    neutral = df_filtrado[df_filtrado['review'] == 1].shape[0]
    positive = df_filtrado[df_filtrado['review'] == 2].shape[0]

    return {'Negative': negative, 'Neutral': neutral, 'Positive': positive}