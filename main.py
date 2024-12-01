from http.server import BaseHTTPRequestHandler, HTTPServer
from load_data import load_all_data
from simulation import simulate_shipments_with_clustering
from truck_operations import create_new_truck
from Models.Driver import Driver
import folium as fo
import json
import os
import shutil

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/generar_ruta':
            # Load data
            locations, products, clients, connections, lines, shipments, constants = load_all_data()

            # Create a driver manually since it is not loaded from the database
            driver = Driver(driver_id=1, name='Driver A', hourly_pay=constants[0].get_drivers_hourly_pay())

            # Start with one truck
            trucks = [create_new_truck(1, driver, constants)]

            # Run the simulation
            routes, total_cost, discarded_shipments = simulate_shipments_with_clustering(trucks, shipments, constants, connections, locations)

            # Clear the Maps folder
            maps_folder = 'Maps'
            if os.path.exists(maps_folder):
                shutil.rmtree(maps_folder)
            os.makedirs(maps_folder)

            # Create the general map centered in Spain
            general_map = fo.Map(location=[40.0, -3.0], zoom_start=6)

            # Extract coordinates for locations
            location_coords = {location.get_name(): (location.get_latitude(), location.get_longitude()) for location in locations}

            # List of vibrant colors for trucks (compatible with folium.Icon)
            truck_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue', 'darkblue', 'darkgreen', 'black']

            # Draw routes from simulation and generate individual maps for each truck
            for index, truck_route in enumerate(routes):
                delivery_points = truck_route["delivery_points"]
                full_route = truck_route["full_route"]

                # Assign a color for each truck based on its index
                truck_color = truck_colors[index % len(truck_colors)]

                # Highlight the full route on the general map with the truck's color
                route_coords = [location_coords[loc_name] for loc_name in full_route if loc_name in location_coords]
                fo.PolyLine(locations=route_coords, color=truck_color, weight=5, opacity=0.8).add_to(general_map)

                # Add warehouse icons for each delivery point on the general map
                for point in delivery_points:
                    if point in location_coords:
                        fo.Marker(
                            location=location_coords[point],
                            popup=point,
                            icon=fo.Icon(icon='warehouse', color=truck_color, prefix='fa')
                        ).add_to(general_map)

                # Create an individual map for this truck
                individual_map = fo.Map(location=[40.0, -3.0], zoom_start=6)
                fo.PolyLine(locations=route_coords, color=truck_color, weight=5, opacity=0.8).add_to(individual_map)

                # Add markers for each delivery point in the route with numbers indicating order on the individual map
                for order, point in enumerate(full_route, start=1):
                    if point in location_coords:
                        # Calculate offset for markers to avoid overlap
                        offset_lat = 0.004 * (order % 2)  # Alternating latitude offset
                        offset_lng = 0.004 * (order % 3)  # Alternating longitude offset

                        # Marker for order number with color and black border for individual map only
                        marker_html = f"""
                            <div style="font-size: 14pt; color: {truck_color}; font-weight: bold; text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;">
                                {order}
                            </div>
                        """

                        # Add the order number above the marker with offset to the individual map
                        fo.Marker(
                            location=(
                                location_coords[point][0] + offset_lat,
                                location_coords[point][1] + offset_lng
                            ),
                            icon=fo.DivIcon(html=marker_html)
                        ).add_to(individual_map)

                        # Add warehouse icon for delivery points to the individual map
                        if point in delivery_points:
                            fo.Marker(
                                location=location_coords[point],
                                popup=point,
                                icon=fo.Icon(icon='warehouse', color=truck_color, prefix='fa')
                            ).add_to(individual_map)

                # Save individual map to Maps folder
                individual_map_path = f'{maps_folder}/Truck_{index + 1}_Route.html'
                individual_map.save(individual_map_path)
                print(f"Mapa individual para el camión {index + 1} guardado en {individual_map_path}")

            # Add a special marker for Mataró to the general map
            if "Mataró" in location_coords:
                fo.Marker(
                    location=location_coords["Mataró"],
                    popup="Mataró",
                    icon=fo.Icon(icon='home', color='blue', prefix='fa')
                ).add_to(general_map)

            # Save the general map to an HTML file
            general_map_path = 'LogisticaPeninsula.html'
            general_map.save(general_map_path)
            print(f"Mapa general guardado en {general_map_path}")

            # Prepare the response data
            discarded_shipments_info = [{
                "shipment_id": shipment.get_shipment_id(),
                "reason": "Expired before delivery" if shipment in discarded_shipments else "No valid path found",
                "product": {"product_id": shipment.get_line().get_product().get_product_id(),
                            "product_name":shipment.get_line().get_product().get_name(),
                            "manufacturing_time":shipment.get_line().get_product().get_manufacturing_time(),
                            "expiration_from_manufacturing":shipment.get_line().get_product().get_expiration_from_manufacturing(),
                            }
            } for shipment in discarded_shipments           
            ]

            response_data = {
                "routes": routes,
                "total_cost": total_cost,
                "discarded_shipments": discarded_shipments_info
            }

            # Send the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Allow cross-origin requests
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
