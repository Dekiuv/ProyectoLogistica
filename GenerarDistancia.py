import csv
import ciudad as ci
import conexiones as co
from math import radians, sin, cos, sqrt, atan2

def calcular_distancia(coord1, coord2):
    """
    Calcula la distancia entre dos coordenadas geográficas usando la fórmula del haversine.

    :param coord1: Tupla (latitud, longitud) de la primera ubicación.
    :param coord2: Tupla (latitud, longitud) de la segunda ubicación.
    :return: Distancia en kilómetros.
    """
    R = 6371  # Radio de la Tierra en km
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def generar_csv_distancias(provincias_espana, Ubicaciones, nombre_archivo):
    """
    Genera un archivo CSV con las distancias entre las ciudades conectadas.

    :param provincias_espana: Diccionario con las ciudades y sus conexiones.
    :param Ubicaciones: Diccionario con las coordenadas de las ciudades.
    :param nombre_archivo: Nombre del archivo CSV a crear.
    """
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["CiudadOrigen", "CiudadDestino", "Distancia (km)"])

        conexiones_escritas = set()

        for origen, destinos in provincias_espana.items():
            for destino in destinos:
                # Evitar duplicados (A->B y B->A)
                clave = tuple(sorted([origen, destino]))
                if clave not in conexiones_escritas:
                    conexiones_escritas.add(clave)
                    
                    if origen in Ubicaciones and destino in Ubicaciones:
                        distancia = calcular_distancia(Ubicaciones[origen], Ubicaciones[destino])
                        writer.writerow([origen, destino, round(distancia, 2)])
                    else:
                        # Si alguna ciudad no tiene coordenadas, indicar "Desconocida"
                        writer.writerow([origen, destino, "Desconocida"])

# Crear el archivo CSV
generar_csv_distancias(co.provincias_espana, ci.Ubicaciones, "DistanciaCiudades.csv")