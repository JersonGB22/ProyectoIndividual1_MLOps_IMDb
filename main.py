# Importación de las librerías necesarias
import pandas as pd
from fastapi import FastAPI

# Importación de los datos
df=pd.read_csv(r"https://raw.githubusercontent.com/JersonGB22/ProyectoIndividual1_Henry/main/Datasets/movie_transformation.csv")

# Instanciamos la clase FastAPI para construir la aplicación de Interfaz de Consultas
app=FastAPI()

# Creación del endpoint de Bienvenida
app.get("/")
def welcome():
    return "Bienvenid@s a mi Proyecto Individual Nº1: Machine Learning Operations (MLOps)"

## Creación de los endpoints

# Función 1: Cantidad de películas producidas por un determinado país en determinado año
app.get("/get_country/{year}/{country}",summary="Cantidad de películas producidas por un determinado país en determinado año")
def get_country(year:int,country:str):
    pass