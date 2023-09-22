# Proyecto 01 - HENRY Labs

## Tabla de Contenido

- [Introducción](#introducción)
- [Objetivos](#objetivos)
- [Stack Tecnológico](#stack-tecnológico)
- [Explicación y Uso del Repositorio](#explicación-y-uso-del-repositorio)

## Introducción
En este proyecto, se asumirá el rol de Data Scientist en Steam, una plataforma multinacional de videojuego para analizar y desarrollar el ciclo de vida completo de un proyecto de Machine Learning. El principal reto a enfrentar es que los datos disponibles tienen una madurez muy baja. Se debe comenzar desde cero, realizando tareas de Data Engineering y desarrollando un MVP (Minimum Viable Product) para el cierre del proyecto.

## Objetivos
* Leer el conjunto de datos con el formato correcto, eliminando columnas innecesarias para optimizar el rendimiento de la API y el entrenamiento del modelo.

* Realizar Feature Engineering creando una columna llamada 'sentiment_analysis' que refleje el análisis de sentimiento de las reseñas de usuarios, facilitando así el trabajo de los modelos de machine learning.

* Desarrollar una API utilizando el framework FastAPI para exponer los datos de la empresa y permitir consultas específicas, como obtener información sobre el gasto de un usuario, el porcentaje de recomendación, clasificaciones de género y más.

* Implementar la API para que sea accesible desde la web, utilizando servicios como Render o Railway.

* Realizar un Análisis Exploratorio de Datos (EDA) manual, investigando las relaciones entre variables, identificando outliers y patrones interesantes en el dataset.

* Entrenar un modelo de machine learning que pueda realizar recomendaciones basadas en ítem-ítem o usuario-ítem. Deberás crear funciones en la API para acceder a estas recomendaciones.

* Presentar tus resultados en un video que muestre el funcionamiento de la API y explique el modelo utilizado para el sistema de recomendación.

## Stack Tecnológico
El stack tecnológico utilizado para este proyecto fue el siguiente:
* Visual Studio Code (Editor de codigo en donde se manipuló archivos .py y . ipynb)
* Las librerias requeridas para el funcionamiento del proyecto las cuales se encuentran detalladas en el archivo requirements.txt de este repositorio.
* FastPAI el cual es un marco web de Python de código abierto y de alto rendimiento utilizado para crear aplicaciones web API de forma rápida y eficiente
* Render el cual es un servicio en la nube que se utiliza para implementar aplicaciones web y sitios web de forma sencilla y escalable.

## Explicación y Uso del Repositorio

### Primer Paso: Extracción y limpieza de datos
Se tienen unos datos en bruto los cuales se encuentran comprimidos en la siguiente carpeta '02_Datasets_PI MLOps_STEAM' en el siguiente link de drive: [Click aqui para descargar los datos](https://drive.google.com/drive/folders/1a1A-WzL5ucw7iMv5r3uZ9SoHzdh1ks8W?usp=sharing), la descomprension de estos datos y sus debidas transformaciones se encuentran en el notebook del presente repositorio llamado 'proyecto_01_EDA_ETL' en los apartados 'Descomprimir datos' y 'Transformación de los dataframes', este notebook esta debidamente detallado y explicado paso por paso como se realizan estas transformaciones y limpieza.

### Segundo Paso: Construir los dataframes para las funciones
El siguiente paso es construir las funciones para los endpoints que se consumiran en la API, para esto se generan los datasets correspondientes para cada función con el fin de generar archivos csv livianos que posteriormente van a ser utilizados en el desarrollo de cada una de las funciones requeridas, la construcción de estos datasets tambien se encuentran en el notebook del presente repositorio llamado 'proyecto_01_EDA_ETL' en el apartado 'Construcción de datasets para las funciones'

### Tercer Paso: Construir el modelo de machine learning
La Construcción modelo de machine learning el modelo tiene una relación ítem-ítem, esto es que se toma un item, en base a que tan similar es ese ítem al resto y se recomiendan similares. la construcción de este modelo tambien se encuentran en el notebook del presente repositorio llamado 'proyecto_01_EDA_ETL' en el apartado 'Modelo de Machine Learning'

### Cuarto Paso: Construir las funciones en el archivo main.py y realizar decoradores
Una vez construidos los dataframes en el archivo 'proyecto_01_EDA_ETL.ipynb' procedemos a exportarlos a formato csv, estos archivos csv estan almacenados en la carpeta '03_datasets_proyecto_01' y van a ser los datos que van a ser consumidos por cada una de las funciones "Cada archivo esta nombrado de acuerdo a la función en donde se vaya a utilizar".
Teniendo la data lista se procede a realizar cada una de las siguiente funciones las cuales estan contenidas y explicadas en el archivo main.py

* Primera funcion: def userdata( User_id : str ): Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a reviews.recommend y cantidad de items.

* Segunda funcion: def countreviews( YYYY-MM-DD y YYYY-MM-DD : str ): Cantidad de usuarios que realizaron reviews entre las fechas dadas y, el porcentaje de recomendación de los mismos en base a reviews.recommend.

* Tercera funcion: def genre( género : str ): Devuelve el puesto en el que se encuentra un género sobre el ranking de los mismos analizado bajo la columna PlayTimeForever.

* Cuarta funcion: def userforgenre( género : str ): Top 5 de usuarios con más horas de juego en el género dado, con su URL (del user) y user_id.

* Quinta funcion:def developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora. 

* Sexta funcion:def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.

* Séptima funcion (Modelo de Machine Learning): def recomendacion_juego( id de producto ): Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.

### Quinto Paso: Subir el proyecto local a github
Se procede subir el proyecto a github mediante la consola bash, tener en cuenta que se creó el archivo .gitignore para que no se suban al repositorio remoto carpetas y archivos que no se requieren para el proyecto. Adicional se creó el archivo requirements.txt el cuál contine todas las librerias utilizadas en el proyecto de tal forma que si desea descargar este proyecto y ponerlo en marcha de manera local debera instalarlas estas librerias para que las funciones trabajen correctamente.

### Sexto Paso: Deployar la aplicación en Render
Proceder a utilizar el servicio Render para que la API pueda ser consumida desde la web, para realizar esta conexión seguir estos pasos: [Click aqui para el paso a paso](https://github.com/HX-FNegrete/render-fastapi-tutorial)

### Séptimo Paso: Screenshots de la API siendo consumida desde la web
Una vez realizado el deploy procedemos a realizar las consultas.

Nota: Actualmente solo estan siendo consumidas las siguientes funciones:

* Segunda funcion: def countreviews( YYYY-MM-DD y YYYY-MM-DD : str ): Cantidad de usuarios que realizaron reviews entre las fechas dadas y, el porcentaje de recomendación de los mismos en base a reviews.recommend.
![Screenshot_Prueba](/04_images_proyecto_01/screenshot_countreviews.png)

* Sexta funcion:def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento.
![Screenshot_Prueba](/04_images_proyecto_01/screenshot_sentiment_analysis.png)
* Séptima funcion (Modelo de Machine Learning): def recomendacion_juego( id de producto ): Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.
![Screenshot_Prueba](/04_images_proyecto_01/screenshot_get_similar_games.png)

## Video Explicativo del Proyecto
El video explicativo del proyecto lo podran encontrar en el siguiente enlace: [Click aqui para ver el video](https://drive.google.com/drive/folders/1a1A-WzL5ucw7iMv5r3uZ9SoHzdh1ks8W?usp=sharing)



