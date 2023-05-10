# Importación de las librerías necesarias
import pandas as pd
from fastapi import FastAPI

# Importación de los datos
df_movie=pd.read_csv(r"https://raw.githubusercontent.com/JersonGB22/ProyectoIndividual1_Henry/main/Datasets/movie_transformation.csv")
# Conversión de la columna 'release_date' a tipo datetime
df_movie["release_date"]=pd.to_datetime(df_movie.release_date)
# Conversión de las columas 'production_countries' y 'production_companies' a tipo list
df_movie["production_countries"]=df_movie.production_countries.apply(lambda x: eval(x))
df_movie["production_companies"]=df_movie.production_companies.apply(lambda x: eval(x))

# Instanciamos la clase FastAPI para construir la aplicación de Interfaz de Consultas
app=FastAPI()

# Creación del endpoint de Bienvenida
@app.get("/")
def welcome():
    return "Bienvenid@s a mi Proyecto Individual Nº1: Machine Learning Operations (MLOps)"

## Creación de los endpoints

#Función 1: Cantidad de peliculas que se estrenaron por nombre de mes
@app.get("/peliculas_mes/{mes}",summary="Cantidad de peliculas que se estrenaron por nombre de mes")
def peliculas_mes(mes:str):
    if mes not in df_movie.release_date.dt.month_name(locale="es").unique():
        return {"Nombre de mes incorrecto. Datos correctos":list(df_movie.release_date.dt.month_name(locale="es").unique())}
    else:
        return {"mes":mes,
                "cantidad":df_movie[df_movie.release_date.dt.month_name(locale="es")==mes].shape[0]}

# Función 2: Cantidad de peliculas que se estrenaron por nombre del día de la semana
@app.get("/peliculas_dia/{dia}",summary="Cantidad de peliculas que se estrenaron por nombre del día de la semana")
def peliculas_dia(dia):
    if dia not in df_movie.release_date.dt.day_name(locale="es").unique():
        return {"Nombre de día de semana incorrecto. Datos correctos":list(df_movie.release_date.dt.day_name(locale="es").unique())}
    else:
        return {"dia":dia,
                "cantidad":df_movie[df_movie.release_date.dt.day_name(locale="es")==dia].shape[0]}

# Función 3: Cantidad de peliculas, ganancia total y promedio por franquicia
# OBSERVACIÓN: La ganancia se tomará del campo 'revenue', que en español significa ganancia
@app.get("/franquicia/{franquicia}",summary="Cantidad de peliculas, ganancia total y promedio por franquicia")
def franquicia(franquicia:str):
    if franquicia not in df_movie.belongs_to_collection.dropna().unique():
        return {"Nombre de franquicia incorrecto. Datos de ejemplo correctos":list(df_movie.belongs_to_collection.dropna().unique())[:10]}
    else:
        df=df_movie[df_movie.belongs_to_collection==franquicia]
        return {"franquicia":franquicia,
                "cantidad":df.shape[0],
                "ganancia_total":int(df.revenue.sum()),
                "ganancia_promedio":float(round(df.revenue.mean(),2))}

# Función 4: Cantidad de películas producidas por país
# OBSERVACIÓN: El país se considerará si se encuentra en la lista de países de la columna "production_countries"
@app.get("/pelicula_pais/{pais}",summary="Cantidad de películas producidas por país")
def peliculas_pais(pais:str):
    if pais not in df_movie.production_countries.explode().dropna().unique():
        return {"Nombre de país inválido. Datos de ejemplo correctos":
                list(df_movie.production_countries.explode().dropna().unique())[:10]}
    else:
        return {"pais":pais,
                "cantidad":df_movie[df_movie.production_countries.apply(lambda x: pais in x)].shape[0]}

# Función 5: Ganancia y cantidad total de peliculas por productora
"""
OBSERVACIÓN: Si en el campo 'production_companies' se encuentra más de una compañía productora, la ganancia (revenue) se considerará
netamente de la productora pedida en la función, puesto que no se tienen datos del porcentaje de ganancia que le corresponde a cada 
productora de películas.
"""
@app.get("/productoras/{productora}",summary="Ganancia y cantidad total de peliculas por productora")
def productoras(productora:str):
    if productora not in df_movie.production_companies.explode().dropna().unique():
        return {"Nombre de productora incorrecto. Datos de ejemplo correctos":
                list(df_movie.production_companies.explode().dropna().unique())[:10]}
    else:
        df=df_movie[df_movie.production_companies.apply(lambda x: productora in x)]
        return {"productora":productora,
                "ganancia_total":int(df.revenue.sum()),
                "cantidad":df.shape[0]}

# Función 6: Inversion, ganancia, retorno y el año de estreno por película
"""
OBSERVACIÓN: El nombre de la película se determinará según el campo 'title'. En situaciones en las que varias películas compartan el mismo nombre, 
como en el caso de Cinderella, se seleccionará aquella que tenga la fecha más reciente de lanzamiento (release_date).
"""
@app.get("/retorno/{pelicula}",summary="Inversion, ganancia, retorno y año de estreno por película")
def retorno(pelicula):
    if pelicula not in df_movie.title.unique():
        return {"Nombre de película incorrecto. Datos correctos":list(df_movie.title.unique())[:10]}
    else:
        index=df_movie[(df_movie.title==pelicula)].release_date.idxmax()
        return {"pelicula":pelicula,
                "inversion":int(df_movie.loc[index,"budget"]),
                "ganancia":int(df_movie.loc[index,"revenue"]),
                "retorno":float(df_movie.loc[index,"return"]),
                "anio":int(df_movie.loc[index,"release_year"])}