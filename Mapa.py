import folium as fo
import ciudad as ci

# Crear el mapa centrado en España
mapa = fo.Map(location=[40.0, -3.5], zoom_start=6)

# Añadir marcadores para cada ciudad con su popup
for ciudad, coords in ci.Ubicaciones['Ciudades']:
    if ciudad == 'Mataró':  # Cambié a 'Mataró' con tilde, como en tu lista original
        fo.Marker(location=coords, popup=ciudad, icon=fo.Icon(color='red')).add_to(mapa)
    else:
        fo.Marker(location=coords, popup=ciudad, icon=fo.Icon(color='blue')).add_to(mapa)

# Guardar el mapa en un archivo HTML
mapa.save('mapa.html')
