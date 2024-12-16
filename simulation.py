from sklearn.cluster import KMeans
import numpy as np
import datetime
from dijkstra import dijkstra
from truck_operations import create_new_truck, assign_shipments_to_truck, create_next_driver

# Simulate shipments with clustering approach and automatic optimization of clusters
def simulate_shipments_with_clustering(trucks, shipments, constants, connections, locations):
    today = datetime.date.today()
    optimal_clusters = 1
    lowest_cost = float('inf')
    best_truck_routes = []
    best_simulation_cost = 0
    best_discarded_shipments = []  # To track discarded shipments for the best configuration
    best_total_revenue = 0  # To track total revenue for the best configuration
    best_net_profit = 0  # To track net profit for the best configuration

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
        discarded_shipments = []  # Track discarded shipments for this configuration
        total_simulation_cost = 0
        total_revenue = 0  # Track total revenue for this configuration

        # Iterate through each cluster and simulate shipments for that cluster
        for cluster_label, cluster_shipments in clusters.items():
            if not cluster_shipments:
                continue

            # Sort shipments in cluster by closest expiration date
            #shipments_sorted = sorted(cluster_shipments, key=lambda s: s.get_line().get_product().get_manufacturing_time() + s.get_line().get_product().get_expiration_from_manufacturing())
            shipments_sorted = sorted(cluster_shipments, key=lambda s: s.get_line().get_product().get_expiration_from_manufacturing())

            # Allocate shipments to trucks
            while shipments_sorted:
                current_truck = create_new_truck(len(used_trucks) + 1, create_next_driver(), constants)
                used_trucks.append(current_truck)

                route = []  # Complete route including intermediate points
                delivery_points = []  # Only final delivery points (i.e., shipment destinations)
                route_cost = 0
                truck_shipments = []  # Track the shipments assigned to this truck

                # Continue assigning shipments until truck capacity is reached or shipments are exhausted
                while shipments_sorted:
                    shipment = shipments_sorted[0]
                    location = shipment.get_location()
                    product = shipment.get_line().get_product()
                    # expiration_date = today + datetime.timedelta(days=product.get_manufacturing_time() + product.get_expiration_from_manufacturing())
                    expiration_date = today + datetime.timedelta(days=product.get_expiration_from_manufacturing())
                    days_until_expiration = (expiration_date - today).days

                    # Skip shipment if location is None
                    if location is None:
                        print("Warning: Shipment location is None, skipping shipment.")
                        discarded_shipments.append(shipments_sorted.pop(0))
                        continue

                    # Set origin to either the last assigned location or Mataró
                    last_location = current_truck.get_shipments()[-1].get_location() if current_truck.get_shipments() else next((loc for loc in locations if loc.get_name() == 'Mataró'), None)

                    if last_location is None:
                        print("Error: Starting location 'Mataró' not found.")
                        return

                    # Calculate shortest distance and time to the destination using Dijkstra
                    total_time, total_distance, path = dijkstra(locations, connections, last_location.get_name(), location.get_name(), velocity, workday_time, rest_time)

                    # Calculate the total time required in days including rest periods
                    total_days = total_time / workday_time
                    # Check if the shipment can be delivered before product expiration
                    if total_days > days_until_expiration:
                        print(f"Warning: Shipment {shipment.get_shipment_id()} with product {product.get_name()} cannot reach destination on time. Skipping shipment.", 
                              f"Days needed: {total_days}, days_until_expiration: {days_until_expiration}")
                        discarded_shipments.append(shipments_sorted.pop(0))
                        continue

                    # Calculate the costs for this route
                    fuel_cost = total_distance * fuel_cost_per_km
                    driver_cost = total_time * drivers_hourly_pay
                    total_route_cost = fuel_cost + driver_cost

                    # Accumulate total cost of all routes in the simulation
                    total_simulation_cost += total_route_cost
                    route_cost += total_route_cost

                    # Calculate the revenue generated from the shipment
                    revenue = shipment.get_line().get_quantity() * product.get_price()
                    total_revenue += revenue

                    # Check the truck capacity and assign shipments accordingly
                    total_quantity = shipment.get_line().get_quantity()
                    if current_truck.get_capacity() >= total_quantity:
                        assign_shipments_to_truck(current_truck, [shipment])
                        truck_shipments.append({
                            "shipment_id": shipment.get_shipment_id(),
                            "quantity": shipment.get_line().get_quantity(),
                            "product": {
                                "product_id": product.get_product_id(),
                                "name": product.get_name(),
                                "expiration": product.get_expiration_from_manufacturing(),
                                "manufacturing_time": product.get_manufacturing_time(),
                                "price": product.get_price()
                            }
                        })
                        delivery_points.append(location.get_name())
                        shipments_sorted.pop(0)  # Remove assigned shipment from the list
                    else:
                        # If current truck cannot accommodate the shipment, break and start a new truck
                        break

                    # Update route information, including all intermediate locations
                    for loc in path:
                        if loc.get_name() not in route:
                            route.append(loc.get_name())

                # Calculate the cost and route for returning to Mataró
                return_route = []
                return_route_cost = 0
                if delivery_points:
                    last_location = route[-1]
                    mataró_location = next((loc for loc in locations if loc.get_name() == 'Mataró'), None)

                    if last_location and mataró_location:
                        return_time, return_distance, return_path = dijkstra(locations, connections, last_location, "Mataró", velocity, workday_time, rest_time)
                        
                        # Calculate the costs for returning to Mataró
                        return_fuel_cost = return_distance * fuel_cost_per_km
                        return_driver_cost = return_time * drivers_hourly_pay
                        return_route_cost = return_fuel_cost + return_driver_cost

                        # Accumulate the return cost to the total cost
                        total_simulation_cost += return_route_cost
                        route_cost += return_route_cost
                        return_route = []
                        for loc in return_path:
                            return_route.append(loc.get_name())
                        
                # Store truck route, cost, shipment, and product information only if it has shipments
                if truck_shipments:
                    truck_routes.append({
                        "truck_id": current_truck.get_truck_id(),
                        "delivery_points": delivery_points,
                        "full_route": route,
                        "route_to_mataró": return_route,
                        "route_cost": route_cost,
                        "driver": current_truck.get_driver().get_name(),
                        "total_shipments": len(truck_shipments),
                        "shipments": truck_shipments
                    })

        # Check if the current clustering configuration has a lower cost
        net_profit = total_revenue - total_simulation_cost
        if total_simulation_cost < lowest_cost:
            lowest_cost = total_simulation_cost
            optimal_clusters = num_clusters
            best_truck_routes = truck_routes
            best_simulation_cost = total_simulation_cost
            best_discarded_shipments = discarded_shipments
            best_total_revenue = total_revenue
            best_net_profit = net_profit

    # Print the optimal configuration and truck routes
    print(f"Optimal number of clusters: {optimal_clusters}")
    print(f"Total cost of all shipments (including return to Mataró): {best_simulation_cost:.2f} €")
    print(f"Total revenue from all shipments: {best_total_revenue:.2f} €")
    print(f"Net profit from all shipments: {best_net_profit:.2f} €")
    print(f"Number of discarded shipments: {len(best_discarded_shipments)}")

    for truck_route in best_truck_routes:
        print(f"Truck {truck_route['truck_id']}")
        print(f"Route Cost: {truck_route['route_cost']:.2f} €")
        print(f"Driver: {truck_route['driver']}")
        print(f"Delivery Points: {truck_route['delivery_points']}")
        print(f"Full Route: {truck_route['full_route']}")
        print(f"Route to Mataró: {truck_route['route_to_mataró']}")
        print(f"Total Shipments: {truck_route['total_shipments']}")
        print(f"Shipments on truck: {truck_route['shipments']}")

    return best_truck_routes, best_simulation_cost, best_discarded_shipments, best_total_revenue, best_net_profit
