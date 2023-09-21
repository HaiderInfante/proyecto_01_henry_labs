import pandas as pd
from fastapi import FastAPI
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#FastAPI
app = FastAPI()

@app.get("/")
def root():

    return {"message": "Hola como estas, bienvenido al proyecto numero 1 del Bootcamp de Henry\nAhora"}
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

# Cargar los archivos para la funcion del modelo de machine learning
df_model_machine_learning = pd.read_csv('03_datasets_proyecto_01/model_machine_learning_file_one.csv')

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
    convert_genre = genres.lower()

    # Filtrar el DataFrame por género
    filter_third_function = df_third_function['genres'].str.lower() == convert_genre

    # Obtener el ranking si se encuentra el género
    if filter_third_function.any():
        ranking = df_third_function.loc[filter_third_function, 'ranking'].iloc[0]
        return {'ranking': ranking}
    else:
        return "Genero no encontrado."

# # Fourth Function: def userforgenre( género : str ): Top 5 de usuarios con más horas de juego en el género dado, 
# #                  con su URL (del user) y user_id.

@app.get('/userforgenre/{genre}')
def userforgenre(genre:str):
# Filtra por el género deseado
    genero_buscado = genre.lower()

    # Filtrar el DataFrame por género (insensible a mayúsculas/minúsculas)
    filtered_df = df_fourth_function[df_fourth_function['genres'].str.lower() == genero_buscado]

    # Verifica si el género se encontró en el DataFrame
    if not filtered_df.empty:
        # Ordena el DataFrame filtrado por 'playtime_forever' en orden descendente
        sorted_df = filtered_df.sort_values(by='playtime_forever', ascending=False)

        # Toma los primeros 5 usuarios y almacénalos en una lista
        top_5_users_list = sorted_df.head(5)['user_id'].tolist()
        top_5_users_url_list = sorted_df.head(5)['user_url'].tolist()

        return {'user_id': top_5_users_list, 'user_url': top_5_users_url_list}
    else:
        return "Genero no encontrado"  # Retorna None si el género no se encontró en el archivo CSV

# # Fifth_Function: def developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free por año
# #                                según empresa desarrolladora. Ejemplo de salida:

@app.get('/developer/{developer_parameter}')
def developer(developer_parameter:str):
    filtered_df = df_fifth_function[df_fifth_function['developer'] == developer_parameter]
    # Agrupar por año y contar la cantidad de elementos
    filtered_df['release_date'] = pd.to_datetime(filtered_df['release_date'])
    grouped = filtered_df.groupby(filtered_df['release_date'].dt.year)['price'].count().reset_index()

    # Calcular el porcentaje de contenido Free To Play por año
    total_items_por_ano = grouped['price'].sum()
    free_to_play_items_por_ano = filtered_df[filtered_df['price'] == 'Free To Play'].groupby(filtered_df['release_date'].dt.year)['price'].count().reset_index()
    free_to_play_items_por_ano.rename(columns={'price': 'free_to_play_count'}, inplace=True)
    merged = pd.merge(grouped, free_to_play_items_por_ano, on='release_date', how='left').fillna(0)
    merged['porcentaje_free_to_play'] = (merged['free_to_play_count'] / merged['price']) * 100

    # Crear el diccionario de resultados
    final_result = {
        'year': merged['release_date'].tolist(),
        'total_items_count': merged['price'].tolist(),
        'free_to_play_percentage': merged['porcentaje_free_to_play'].tolist()
    }

    return final_result

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

@app.get('/get_similar_games/{game_id}')
def get_similar_games(game_id:int):
    df_model_machine_learning['tags'] = df_model_machine_learning['tags'].apply(lambda x: eval(x))
    num_recommendations=5
    # Obtener las etiquetas del juego de referencia
    tags = df_model_machine_learning.loc[df_model_machine_learning['id'] == game_id, 'tags'].iloc[0]

    # Crear una matriz de características basada en las etiquetas
    vectorizer = CountVectorizer()
    tag_matrix = vectorizer.fit_transform(df_model_machine_learning['tags'].apply(lambda x: ' '.join(x)))

    # Calcular la similitud coseno entre juegos basada en las etiquetas
    similarity_scores = cosine_similarity(tag_matrix)

    # Obtener el índice del juego de referencia
    game_index = df_model_machine_learning[df_model_machine_learning['id'] == game_id].index[0]

    # Obtener las puntuaciones de similitud para el juego de referencia
    game_similarity_scores = similarity_scores[game_index]

    # Obtener los índices de los juegos más similares (excluyendo el juego de referencia)
    similar_game_indices = game_similarity_scores.argsort()[::-1][1:num_recommendations+1]

    # Obtener la lista de juegos recomendados
    recommended_games = df_model_machine_learning.iloc[similar_game_indices]['title'].tolist()

    return {'recommended_games': recommended_games}