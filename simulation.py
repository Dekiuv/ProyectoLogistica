from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from dijkstra import dijkstra
from truck_operations import create_new_truck, assign_shipments_to_truck, create_next_driver
import datetime

# Simulate shipments with clustering approach and automatic optimization of clusters
def simulate_shipments_with_clustering(trucks, shipments, constants, connections, locations):
    today = datetime.date.today()
    optimal_clusters = 1
    lowest_cost = float('inf')
    best_truck_routes = []
    best_simulation_cost = 0

    # Constants for the simulation
    velocity = constants[0].get_velocity()  # Velocity of the truck in km/h
    workday_time = constants[0].get_workday_time()  # Workday duration in hours
    rest_time = constants[0].get_rest_time()  # Rest duration in hours
    fuel_cost_per_km = constants[0].get_fuel_cost_km()  # Fuel cost per km
    drivers_hourly_pay = constants[0].get_drivers_hourly_pay()  # Cost per hour for drivers

    # Extract coordinates from locations
    coordinates = np.array([(location.get_latitude(), location.get_longitude()) for location in locations])

    # Iterate through possible numbers of clusters to find the optimal one
    for num_clusters in range(1, len(locations)):  # Try from 1 to len(locations) clusters
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(coordinates)
        labels = kmeans.labels_

        # Create clusters of shipments based on their location's cluster label
        location_id_to_cluster = {location.get_location_id(): label for location, label in zip(locations, labels)}
        clusters = {i: [] for i in range(num_clusters)}

        for shipment in shipments:
            location = shipment.get_location()
            if location:
                cluster_label = location_id_to_cluster[location.get_location_id()]
                clusters[cluster_label].append(shipment)

        # Simulate shipments for this clustering configuration
        used_trucks = []
        assigned_locations = set()
        truck_routes = []
        total_simulation_cost = 0

        # Iterate through each cluster and simulate shipments for that cluster
        for cluster_label, cluster_shipments in clusters.items():
            if not cluster_shipments:
                continue

            # Sort shipments in cluster by closest expiration date
            shipments_sorted = sorted(cluster_shipments, key=lambda s: s.get_line().get_product().get_manufacturing_time() + s.get_line().get_product().get_expiration_from_manufacturing())

            # Create a new truck for each cluster (or reuse if possible)
            current_truck = create_new_truck(len(used_trucks) + 1, create_next_driver(), constants)
            used_trucks.append(current_truck)

            route = []  # Complete route including intermediate points
            delivery_points = []  # Only final delivery points (i.e., shipment destinations)
            route_cost = 0

            for shipment in shipments_sorted:
                location = shipment.get_location()
                product = shipment.get_line().get_product()
                expiration_date = today + datetime.timedelta(days=product.get_manufacturing_time() + product.get_expiration_from_manufacturing())
                days_until_expiration = (expiration_date - today).days

                # Skip shipment if location is None
                if location is None:
                    print("Warning: Shipment location is None, skipping shipment.")
                    continue

                # Skip if location already assigned to a truck
                if location in assigned_locations:
                    continue

                # Find all shipments for the same location
                same_location_shipments = [s for s in shipments_sorted if s.get_location() == location]

                # Set origin to either the last assigned location or Mataró
                last_location = current_truck.get_shipments()[-1].get_location() if current_truck.get_shipments() else next((loc for loc in locations if loc.get_name() == 'Mataró'), None)

                if last_location is None:
                    print("Error: Starting location 'Mataró' not found.")
                    return

                # Calculate shortest distance and time to the destination using Dijkstra
                total_time_with_rest, total_distance, path = dijkstra(locations, connections, last_location.get_name(), location.get_name(), velocity, workday_time, rest_time)

                # Check if no path was found
                if total_distance == float('inf'):
                    print(f"Warning: No valid path found from {last_location.get_name()} to {location.get_name()}. Skipping shipment.")
                    continue

                # Calculate number of rest periods needed
                num_rest_periods = int(total_time_with_rest / workday_time)
                total_rest_time = num_rest_periods * rest_time

                # Final time including the rest time
                total_time_with_rest = (total_distance / velocity) + total_rest_time
                days_needed = total_time_with_rest / workday_time

                # Check if the shipment can be delivered before product expiration
                if days_needed > days_until_expiration:
                    print(f"Warning: Shipment {shipment.get_shipment_id()} with product {product.get_name()} cannot reach destination on time. Skipping shipment.", 
                          f"Days needed: {days_needed}, days_until_expiration: {days_until_expiration}")
                    continue

                # Calculate the costs for this route
                fuel_cost = total_distance * fuel_cost_per_km
                driver_cost = (total_time_with_rest) * drivers_hourly_pay
                total_route_cost = fuel_cost + driver_cost

                # Accumulate total cost of all routes in the simulation
                total_simulation_cost += total_route_cost
                route_cost += total_route_cost

                # Assign the shipments to the current truck
                total_quantity = sum(s.get_line().get_quantity() for s in same_location_shipments)
                if current_truck.get_capacity() >= total_quantity:
                    assign_shipments_to_truck(current_truck, same_location_shipments)
                    assigned_locations.add(location)
                else:
                    # If the current truck cannot handle the shipment, create a new truck for overflow
                    new_truck = create_new_truck(len(used_trucks) + 1, create_next_driver(), constants)
                    assign_shipments_to_truck(new_truck, same_location_shipments)
                    assigned_locations.add(location)
                    used_trucks.append(new_truck)

                # Update route information, including all intermediate locations
                for loc in path:
                    if loc.get_name() not in route:
                        route.append(loc.get_name())

                # Add the final delivery point
                delivery_points.append(location.get_name())

            # Store truck route and cost information
            truck_routes.append({
                "truck_id": current_truck.get_truck_id(),
                "route": " -> ".join(route),  # Full route including intermediate points
                "delivery_points": delivery_points,  # Only delivery points
                "full_route": route,  # List of all route points (intermediate and final)
                "route_cost": route_cost,
                "driver": current_truck.get_driver().get_name()
            })

        # Check if the current clustering configuration has a lower cost
        if total_simulation_cost < lowest_cost:
            lowest_cost = total_simulation_cost
            optimal_clusters = num_clusters
            best_truck_routes = truck_routes
            best_simulation_cost = total_simulation_cost

    # Print the optimal configuration and truck routes
    print(f"Optimal number of clusters: {optimal_clusters}")
    print(f"Total cost of all shipments: {best_simulation_cost:.2f} €")

    for truck_route in best_truck_routes:
        print(f"Truck {truck_route['truck_id']} Route: {truck_route['route']}")
        print(f"Route Cost: {truck_route['route_cost']:.2f} €")
        print(f"Driver: {truck_route['driver']}")
        print(f"Delivery Points: {truck_route['delivery_points']}")
        print(f"Full Route: {truck_route['full_route']}")

    return best_truck_routes, best_simulation_cost
