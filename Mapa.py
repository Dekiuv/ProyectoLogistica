import folium as fo
import ciudad as ci
from conexiones import *
# Crear el mapa centrado en España
mapa = fo.Map(location=[40.0, -3.5], zoom_start=6)

# Diccionario con las coordenadas de cada ciudad (esto es solo un ejemplo, debes completarlo)


# Lista de conexiones, generada previamente con la función listar_conexiones
conexiones = listar_conexiones(provincias_espana)

# Añadir marcadores para cada ciudad con su popup
for ciudad, coords in ci.Ubicaciones.items():
    color = 'red' if ciudad == 'Mataro' else 'blue'
    fo.Marker(location=coords, popup=ciudad, icon=fo.Icon(color=color)).add_to(mapa)

# Dibujar las líneas entre las conexiones
for (ciudad1, ciudad2) in conexiones:
    if ciudad1 in ci.Ubicaciones and ciudad2 in ci.Ubicaciones:
        coords1 = ci.Ubicaciones[ciudad1]
        coords2 = ci.Ubicaciones[ciudad2]
        
        # Añadir una línea entre las dos ciudades
        fo.PolyLine(locations=[coords1, coords2], color='green', weight=2.5, opacity=0.7).add_to(mapa)

# Guardar el mapa en un archivo HTML
mapa.save('mapa.html')
