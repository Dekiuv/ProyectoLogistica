from http.server import BaseHTTPRequestHandler, HTTPServer
from load_data import load_all_data
from simulation import simulate_shipments_with_clustering
from truck_operations import create_new_truck
from Models.Driver import Driver
from Models.Constant import Constant
import folium as fo
import json
import os
import shutil

# Declaración global de 'constants' como un objeto Constant (inicialmente None)
constants = None

# Array of predefined truck colors that Folium supports
truck_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue', 'darkblue', 'darkgreen', 'black']

class RequestHandler(BaseHTTPRequestHandler):

    # Manejar solicitudes OPTIONS para CORS
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    # Manejar solicitudes POST para establecer constantes
    def do_POST(self):
        global constants
        if self.path == '/set_constants':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            # Crear un objeto Constant con los valores recibidos
            constants = [Constant(
                constant_id=1,
                velocity=data.get('velocity', 90),
                workday_time=data.get('workdayTime', 8),
                rest_time=data.get('restTime', 16),
                drivers_hourly_pay=data.get('driversHourlyPay', 15),
                fuel_cost_km=data.get('fuelCostKm', 1.5),
                truck_capacity=data.get('truckCapacity', 2000)
            )]

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = json.dumps(constants[0].__dict__)
            self.wfile.write(response.encode('utf-8'))

    def do_GET(self):
        global constants
        if self.path == '/generar_ruta':
            if constants is None:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_message = {"error": "Las constantes no se han establecido. Por favor, envíe los valores primero."}
                self.wfile.write(json.dumps(error_message).encode('utf-8'))
                return

            # Load data
            locations, products, clients, connections, lines, shipments = load_all_data()

            # Crear un conductor manualmente ya que no se carga desde la base de datos
            driver = Driver(driver_id=1, name='Driver A', hourly_pay=constants[0].get_drivers_hourly_pay())

            # Iniciar con un camión
            trucks = [create_new_truck(1, driver, constants)]

            # Ejecutar la simulación
            routes, total_cost, discarded_shipments, best_total_revenue, best_net_profit = simulate_shipments_with_clustering(trucks, shipments, constants, connections, locations)

            # Limpiar la carpeta Maps
            maps_folder = 'Maps'
            if os.path.exists(maps_folder):
                shutil.rmtree(maps_folder)
            os.makedirs(maps_folder)

            # Crear el mapa general centrado en España
            general_map = fo.Map(location=[40.0, -3.0], zoom_start=6)

            # Extraer coordenadas para las ubicaciones
            location_coords = {location.get_name(): (location.get_latitude(), location.get_longitude()) for location in locations}

            # Dibujar rutas de la simulación y generar mapas individuales para cada camión
            for index, truck_route in enumerate(routes):
                delivery_points = truck_route["delivery_points"]
                full_route = truck_route["full_route"]

                # Obtener el color para el camión basado en su índice
                truck_color = truck_colors[index % len(truck_colors)]

                # Resaltar la ruta completa en el mapa general con el color del camión
                route_coords = [location_coords[loc_name] for loc_name in full_route if loc_name in location_coords]
                fo.PolyLine(locations=route_coords, color=truck_color, weight=5, opacity=0.8).add_to(general_map)

                # Añadir iconos de almacén para cada punto de entrega en el mapa general
                for point in delivery_points:
                    if point in location_coords:
                        fo.Marker(
                            location=location_coords[point],
                            popup=point,
                            icon=fo.Icon(icon='warehouse', color=truck_color, prefix='fa')
                        ).add_to(general_map)

                # Crear un mapa individual para este camión
                individual_map = fo.Map(location=[40.0, -3.0], zoom_start=6)
                fo.PolyLine(locations=route_coords, color=truck_color, weight=5, opacity=0.8).add_to(individual_map)

                # Añadir marcadores para cada punto de entrega en la ruta con números indicando el orden en el mapa individual
                for order, point in enumerate(full_route, start=1):
                    if point in location_coords:
                        offset_lat = 0.004 * (order % 2)
                        offset_lng = 0.004 * (order % 3)

                        marker_html = f"""
                            <div style="font-size: 14pt; color: {truck_color}; font-weight: bold; text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;">
                                {order}
                            </div>
                        """

                        fo.Marker(
                            location=(
                                location_coords[point][0] + offset_lat,
                                location_coords[point][1] + offset_lng
                            ),
                            icon=fo.DivIcon(html=marker_html)
                        ).add_to(individual_map)

                        if point in delivery_points:
                            fo.Marker(
                                location=location_coords[point],
                                popup=point,
                                icon=fo.Icon(icon='warehouse', color=truck_color, prefix='fa')
                            ).add_to(individual_map)

                # Guardar el mapa individual en la carpeta Maps
                individual_map_path = f'{maps_folder}/Truck_{truck_route["truck_id"]}_Route.html'
                individual_map.save(individual_map_path)
                print(f"Mapa individual para el camión {index + 1} guardado en {individual_map_path}")

            # Añadir un marcador especial para Mataró en el mapa general
            if "Mataró" in location_coords:
                fo.Marker(
                    location=location_coords["Mataró"],
                    popup="Mataró",
                    icon=fo.Icon(icon='home', color='blue', prefix='fa')
                ).add_to(general_map)

            # Guardar el mapa general en un archivo HTML
            general_map_path = 'LogisticaPeninsula.html'
            general_map.save(general_map_path)
            print(f"Mapa general guardado en {general_map_path}")

            # Preparar los datos de respuesta
            discarded_shipments_info = [{
                "shipment_id": shipment.get_shipment_id(),
                "reason": "Expired before delivery" if shipment in discarded_shipments else "No valid path found",
                "product": {
                    "product_id": shipment.get_line().get_product().get_product_id(),
                    "product_name": shipment.get_line().get_product().get_name(),
                    "manufacturing_time": shipment.get_line().get_product().get_manufacturing_time(),
                    "expiration_from_manufacturing": shipment.get_line().get_product().get_expiration_from_manufacturing(),
                }
            } for shipment in discarded_shipments]

            response_data = {
                "routes": routes,
                "total_cost": total_cost,
                "discarded_shipments": discarded_shipments_info,
                "best_total_revenue": best_total_revenue, 
                "best_net_profit": best_net_profit
            }

            # Enviar la respuesta
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
