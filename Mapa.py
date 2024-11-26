from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import folium as fo
import ciudad as ci
from conexiones import listar_conexiones, dijkstra, provincias_espana

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Responder a las solicitudes OPTIONS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/':
            # Leer la longitud del cuerpo de la solicitud
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parsear el JSON recibido
            data = json.loads(post_data)
            destino = data.get('destino', '')

            # Validar el destino y generar el mapa
            if destino in ci.Ubicaciones:
                # Crear el mapa
                mapa = fo.Map(location=[40.0, -3], zoom_start=6)
                conexiones = listar_conexiones(provincias_espana)

                # Añadir los marcadores
                for ciudad, coords in ci.Ubicaciones.items():
                    icon = fo.Icon(icon='warehouse', color='red', prefix='fa')
                    fo.Marker(location=coords, popup=ciudad, icon=icon).add_to(mapa)

                # Ruta óptima
                ruta_optima = dijkstra(conexiones, ci.Ubicaciones, "Mataro", destino)
                ruta_coords = [ci.Ubicaciones[ciudad] for ciudad in ruta_optima]
                fo.PolyLine(locations=ruta_coords, color='green', weight=5, opacity=0.8).add_to(mapa)

                # Guardar el mapa en un archivo HTML
                mapa_url = 'LogisticaPeninsula.html'
                mapa.save(mapa_url)

                # Responder con éxito
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'mapa_url': mapa_url}).encode())
            else:
                # Responder con error
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': f"La ciudad {destino} no está en la lista."}).encode())

# Ejecutar el servidor
server = HTTPServer(('localhost', 5000), RequestHandler)
print("Servidor ejecutándose en http://localhost:5000")
server.serve_forever()
