from load_data import load_all_data
from simulation import simulate_shipments_with_clustering
from truck_operations import create_new_truck
from Models.Driver import Driver
from dijkstra import dijkstra
import folium as fo

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
    for order, delivery_point in enumerate(full_route, start=1):
        if delivery_point in location_coords:
            # Track delivery points
            delivery_locations.add(delivery_point)

            # Determine offset based on the number of times this location has been visited
            if delivery_point not in location_visits:
                location_visits[delivery_point] = {
                    "count": 0,
                    "colors": []
                }

            # Increment visit count and store color
            location_visits[delivery_point]["count"] += 1
            location_visits[delivery_point]["colors"].append(truck_color)

            offset_index = location_visits[delivery_point]["count"] - 1

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
                    location_coords[delivery_point][0] + offset_lat,
                    location_coords[delivery_point][1] + offset_lng
                ),
                icon=fo.DivIcon(html=f"""
                    <div style="font-size: 14pt; color: {truck_color}; font-weight: bold; text-shadow: -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000, 2px 2px 0 #000;">
                        {order}
                    </div>
                """)
            ).add_to(mapa)

# Add markers with the color of the route that visited the point
for location, data in location_visits.items():
    if location in location_coords:
        if location == "Mataró":
            # For Mataró, use a different icon and color to indicate the start
            fo.Marker(
                location=location_coords[location],
                popup=location,
                icon=fo.Icon(icon='home', color='blue', prefix='fa')
            ).add_to(mapa)
        else:
            # Assign the truck color that passed by this location
            marker_color = data["colors"][-1]  # Use the last visiting truck's color as the primary color

            # Use folium Icon with Font Awesome 'warehouse' and the truck's color
            fo.Marker(
                location=location_coords[location],
                popup=location,
                icon=fo.Icon(icon='warehouse', color=marker_color, prefix='fa')
            ).add_to(mapa)

# Draw connections between only involved locations (in the full route, not as markers)
for connection in connections:
    loc1 = connection.get_location1()
    loc2 = connection.get_location2()
    if loc1 and loc2:
        name1 = loc1.get_name()
        name2 = loc2.get_name()
        # Only draw connections between locations that are actually used in routes
        if name1 in delivery_locations and name2 in delivery_locations:
            coords1 = location_coords.get(name1)
            coords2 = location_coords.get(name2)
            if coords1 and coords2:
                fo.PolyLine(locations=[coords1, coords2], color='gray', weight=2.5, opacity=0.5).add_to(mapa)

# Save the map to an HTML file
mapa.save('LogisticaPeninsula.html')

print("Mapa guardado en LogisticaPeninsula.html")
