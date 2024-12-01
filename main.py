from http.server import BaseHTTPRequestHandler, HTTPServer
from load_data import load_all_data
from simulation import simulate_shipments_with_clustering
from truck_operations import create_new_truck
from Models.Driver import Driver
import folium as fo
import json

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
            routes, total_cost = simulate_shipments_with_clustering(trucks, shipments, constants, connections, locations)

            # Create the map centered in Spain
            mapa = fo.Map(location=[40.0, -3.0], zoom_start=6)

            # Extract coordinates for locations
            location_coords = {location.get_name(): (location.get_latitude(), location.get_longitude()) for location in locations}

            # List of vibrant colors for trucks (compatible with folium.Icon)
            truck_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'cadetblue', 'darkblue', 'darkgreen', 'black']

            # Set to keep track of all locations involved in deliveries (final delivery points)
            delivery_locations = set()

            # Dictionary to keep track of the number of times each location has been visited and their colors
            location_visits = {}

            # Draw routes from simulation
            for index, truck_route in enumerate(routes):
                delivery_points = truck_route["delivery_points"]
                full_route = truck_route["full_route"]

                # Assign a color for each truck based on its index
                truck_color = truck_colors[index % len(truck_colors)]

                # Highlight the full route with the truck's color
                route_coords = [location_coords[loc_name] for loc_name in full_route if loc_name in location_coords]
                fo.PolyLine(locations=route_coords, color=truck_color, weight=5, opacity=0.8).add_to(mapa)

                # Add markers for each delivery point in the route with numbers indicating order
                for order, point in enumerate(full_route, start=1):
                    if point in location_coords:
                        # Determine if the point is a final delivery point or an intermediate one
                        if point in delivery_points:
                            # Track delivery points
                            delivery_locations.add(point)

                            # Determine offset based on the number of times this location has been visited
                            if point not in location_visits:
                                location_visits[point] = {
                                    "count": 0,
                                    "colors": []
                                }

                            # Increment visit count and store color
                            location_visits[point]["count"] += 1
                            location_visits[point]["colors"].append(truck_color)

                            offset_index = location_visits[point]["count"] - 1

                            # Calculate offset for the label to prevent overlap (increase offset for better separation)
                            offset_lat = 0.004 * (offset_index + 1)  # Significant increase in latitude offset per visit
                            offset_lng = 0.004 * (offset_index + 1)  # Significant increase in longitude offset per visit

                            # Alternate offset direction for better distribution
                            if offset_index % 2 == 0:
                                offset_lat = -offset_lat
                            if (offset_index // 2) % 2 == 0:
                                offset_lng = -offset_lng

                            # Add the order number above the marker with offset and truck color, including a black border
                            fo.Marker(
                                location=(
                                    location_coords[point][0] + offset_lat,
                                    location_coords[point][1] + offset_lng
                                ),
                                icon=fo.DivIcon(html=f"""
                                    <div style="font-size: 14pt; color: {truck_color}; font-weight: bold; text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;">
                                        {order}
                                    </div>
                                """)
                            ).add_to(mapa)

                            # Use folium Icon with Font Awesome 'warehouse' and the truck's color for final delivery points
                            fo.Marker(
                                location=location_coords[point],
                                popup=point,
                                icon=fo.Icon(icon='warehouse', color=truck_color, prefix='fa')
                            ).add_to(mapa)

            # Add a special marker for Mataró
            if "Mataró" in location_coords:
                fo.Marker(
                    location=location_coords["Mataró"],
                    popup="Mataró",
                    icon=fo.Icon(icon='home', color='blue', prefix='fa')
                ).add_to(mapa)

            # Save the map to an HTML file
            mapa.save('LogisticaPeninsula.html')

            # Prepare the response data
            response_data = {
                "routes": routes,
                "total_cost": total_cost
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
