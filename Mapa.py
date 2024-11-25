import folium as fo
import ciudad as ci
from conexiones import listar_conexiones, dijkstra, provincias_espana

# Crear el mapa centrado en España
mapa = fo.Map(location=[40.0, 3], zoom_start=6)

# Lista de conexiones, generada previamente con la función listar_conexiones
conexiones = listar_conexiones(provincias_espana)

# Añadir marcadores para cada ciudad con su popup y un icono específico
for ciudad, coords in ci.Ubicaciones.items():
    icon_color = 'red'
    # Utilizar un icono de Font Awesome para los marcadores (icono de compás)
    icon = fo.Icon(icon='warehouse', color=icon_color, prefix='fa')
    # Añadir el marcador
    fo.Marker(location=coords, popup=ciudad, icon=icon).add_to(mapa)

# Dibujar las líneas entre las conexiones
for (ciudad1, ciudad2) in conexiones:
    if ciudad1 in ci.Ubicaciones and ciudad2 in ci.Ubicaciones:
        coords1 = ci.Ubicaciones[ciudad1]
        coords2 = ci.Ubicaciones[ciudad2]
        # Añadir una línea entre las dos ciudades
        fo.PolyLine(locations=[coords1, coords2], color='blue', weight=2.5, opacity=0.7).add_to(mapa)

#Menu del usuario
menu = True
while menu:
# Solicitar al usuario la ciudad de destino
    destino = input("Introduce la ciudad de destino: ")
    # Calcular la ruta óptima desde Mataró
    if destino in ci.Ubicaciones:
        ruta_optima = dijkstra(conexiones, ci.Ubicaciones, "Mataro", destino)
        # Pintar la ruta óptima en el mapa
        ruta_coords = [ci.Ubicaciones[ciudad] for ciudad in ruta_optima]
        fo.PolyLine(locations=ruta_coords, color='green', weight=5, opacity=0.8).add_to(mapa)
        # Añadir marcadores especiales para las ciudades en la ruta
        for ciudad in ruta_optima:
            fo.Marker(
                location=ci.Ubicaciones[ciudad],
                popup=ciudad,
                icon=fo.Icon(color="green", icon="warehouse", prefix="fa")
            ).add_to(mapa)
        menu = False
    else:
        print(f"La ciudad {destino} no está en la lista de ubicaciones.")
# Guardar el mapa en un archivo HTML
mapa.save('LogisticaPeninsula.html')