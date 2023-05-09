# Importación de las librerías necesarias
import pandas as pd
from fastapi import FastAPI

# Importación de los datos
df_movie=pd.read_csv(r"https://raw.githubusercontent.com/JersonGB22/ProyectoIndividual1_Henry/main/Datasets/movie_transformation.csv")

# Instanciamos la clase FastAPI para construir la aplicación de Interfaz de Consultas
app=FastAPI()

# Creación del endpoint de Bienvenida
@app.get("/")
def welcome():
    return "Bienvenid@s a mi Proyecto Individual Nº1: Machine Learning Operations (MLOps)"

## Creación de los endpoints

# Función 1: Cantidad de películas producidas por un determinado país en determinado año
# El país se considerará si se encuentra en la lista de países de la columna "production_countries"
@app.get("/get_country/{year}/{country}",summary="Cantidad de películas producidas por un determinado país en determinado año")
def get_country(year:int,country:str):
    if year not in df_movie.release_year.dropna().unique():
        return {"Año de estreno inválido. Rango correcto":[int(df_movie.release_year.min()),int(df_movie.release_year.max())]}
    else:
        df=df_movie[df_movie.release_year==year]
        if country not in df.production_countries.apply(lambda x: eval(x)).explode().dropna().unique():
            return {"Nombre de país inválido. Datos de ejemplo correctos":
                    list(df.production_countries.apply(lambda x: eval(x)).explode().dropna().unique())[:10]}
        else:
            return {"Año":year,"País":country,"Cantidad":df[df.production_countries.apply(lambda x: country in eval(x))].shape[0]}