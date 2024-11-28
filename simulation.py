from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from dijkstra import dijkstra
from truck_operations import create_new_truck, assign_shipments_to_truck
import datetime

# Function to determine optimal number of clusters using the Elbow Method
def determine_optimal_clusters(coordinates):
    inertias = []
    K_range = range(1, 11)  # Probar con 1 a 10 clusters

    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=0).fit(coordinates)
        inertias.append(kmeans.inertia_)

    # Plot the Elbow graph
    plt.figure(figsize=(8, 5))
    plt.plot(K_range, inertias, 'bo-')
    plt.xlabel('Número de Clusters (k)')
    plt.ylabel('Inercia')
    plt.title('Método del Codo para encontrar el número óptimo de clusters')
    plt.show()

    # Find the "elbow" point programmatically (simplified heuristic)
    optimal_k = K_range[inertias.index(min(inertias, key=lambda x: abs(x - np.mean(inertias))))]

    return optimal_k

# Simulate shipments with clustering approach
def simulate_shipments_with_clustering(trucks, shipments, constants, connections, locations, driver):
    today = datetime.date.today()
    used_trucks = []
    assigned_locations = set()
    truck_routes = []
    total_simulation_cost = 0  # Variable to keep track of total cost

    # Extract coordinates from locations
    coordinates = np.array([(location.get_latitude(), location.get_longitude()) for location in locations])

    # Determine the optimal number of clusters
    num_clusters = determine_optimal_clusters(coordinates)
    print(f"Número óptimo de clusters determinado: {num_clusters}")

    # Apply KMeans clustering to group locations
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

    # Constants for the simulation
    velocity = constants[0].get_velocity()  # Velocity of the truck in km/h
    workday_time = constants[0].get_workday_time()  # Workday duration in hours
    rest_time = constants[0].get_rest_time()  # Rest duration in hours
    fuel_cost_per_km = constants[0].get_fuel_cost_km()  # Fuel cost per km
    drivers_hourly_pay = constants[0].get_drivers_hourly_pay()  # Cost per hour for drivers

    # Iterate through each cluster and simulate shipments for that cluster
    for cluster_label, cluster_shipments in clusters.items():
        if not cluster_shipments:
            continue

        # Sort shipments in cluster by closest expiration date
        shipments_sorted = sorted(cluster_shipments, key=lambda s: s.get_line().get_product().get_manufacturing_time() + s.get_line().get_product().get_expiration_from_manufacturing())

        # Create a new truck for each cluster (or reuse if possible)
        current_truck = None
        if len(used_trucks) < num_clusters:
            current_truck = create_new_truck(len(used_trucks) + 1, driver, constants)
            used_trucks.append(current_truck)
        else:
            # Reuse a truck if available
            current_truck = used_trucks[cluster_label]

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
            driver_cost = total_time_with_rest * drivers_hourly_pay
            total_route_cost = fuel_cost + driver_cost

            # Print cost details for each shipment
            print(f"Total distance: {total_distance:.2f} km")
            print(f"  Fuel cost: {fuel_cost:.2f} €")
            print(f"  Driver cost: {driver_cost:.2f} €")
            print(f"  Total route cost: {total_route_cost:.2f} €")

            # Accumulate total cost of all routes in the simulation
            total_simulation_cost += total_route_cost

            # Assign the shipments to the current truck
            total_quantity = sum(s.get_line().get_quantity() for s in same_location_shipments)
            if current_truck.get_capacity() >= total_quantity:
                assign_shipments_to_truck(current_truck, same_location_shipments)
                assigned_locations.add(location)
            else:
                # If the current truck cannot handle the shipment, create a new truck for overflow
                new_truck = create_new_truck(len(used_trucks) + 1, driver, constants)
                assign_shipments_to_truck(new_truck, same_location_shipments)
                assigned_locations.add(location)
                used_trucks.append(new_truck)

    # Generate and print routes for each truck
    for truck in used_trucks:
        print(f"Truck {truck.get_truck_id()} is used with shipments:")
        route = []

        for shipment in truck.get_shipments():
            location = shipment.get_location()
            if location is None:
                print("Warning: Shipment location is None, skipping.")
                continue
            print(f"  Shipment {shipment.get_shipment_id()} with product {shipment.get_line().get_product().get_name()} to location {location.get_name()}")
            if location not in route:
                route.append(location)

        # Ensure the route starts from Mataró and then goes to other locations
        origin_location = next((loc for loc in locations if loc.get_name() == 'Mataró'), None)
        if origin_location is not None:
            route.insert(0, origin_location)

        route_str = " -> ".join([loc.get_name() for loc in route if loc is not None])
        print(f"  Route: {route_str}")

        # Store the route
        truck_routes.append({
            "truck_id": truck.get_truck_id(),
            "route": route_str,
            "total_route_cost": total_route_cost  # Store the cost of the route
        })

    print(f"Total trucks used: {len(used_trucks)}")
    print(f"Total cost of all shipments: {total_simulation_cost:.2f}")

    # Return the truck routes and total cost
    return truck_routes, total_simulation_cost
