import osmnx as ox
import networkx as nx
import folium

# Definir las coordenadas de Mataró y Barcelona
origen = (41.5381, 2.4445)  # Mataró
destino = (41.3851, 2.1734)  # Huesca

# Descargar la red vial para la región de interés
G = ox.graph_from_point(origen, dist=300000)

# Encontrar los nodos más cercanos en la red para origen y destino
origen_nodo = ox.distance.nearest_nodes(G, X=origen[1], Y=origen[0])
destino_nodo = ox.distance.nearest_nodes(G, X=destino[1], Y=destino[0])

# Calcular la ruta más corta basada en la longitud de la carretera
ruta = nx.shortest_path(G, origen_nodo, destino_nodo, weight='length')

# Crear el mapa en Folium y añadir la ruta
mapa = folium.Map(location=origen, zoom_start=12)
ruta_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in ruta]
folium.PolyLine(ruta_coords, color='blue', weight=5, opacity=0.7).add_to(mapa)

# Añadir marcadores para origen y destino
folium.Marker(location=origen, popup="Mataró", icon=folium.Icon(color='red')).add_to(mapa)
folium.Marker(location=destino, popup="Barcelona", icon=folium.Icon(color='green')).add_to(mapa)

# Guardar el mapa en un archivo HTML
mapa.save("ruta_mataro_barcelona.html")