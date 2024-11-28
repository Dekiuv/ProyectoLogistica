from load_db_data import *
from Models.Location import Location
from Models.Connection import Connection
from Models.Product import Product
from Models.Line import Line
from Models.Client import Client
from Models.Shipment import Shipment
from Models.Constant import Constant
from Models.Driver import Driver
from Models.Truck import Truck
import datetime
import heapq
import copy

try:
    locations = load_locations()
    print("Locations Loaded:")
    for location in locations:
        print(location)
except TypeError:
    print("Error: Failed to create Location objects. Please check the import path or class definition.")

try:
    products = load_products()
    print("\nProducts Loaded:")
    for product in products:
        print(product)
except TypeError:
    print("Error: Failed to create Product objects. Please check the import path or class definition.")

try:
    clients = load_clients()
    print("\nClients Loaded:")
    for client in clients:
        print(client)
except TypeError:
    print("Error: Failed to create Client objects. Please check the import path or class definition.")

try:
    connections = load_connections()
    print("\nConnections Loaded:")
    for connection in connections:
        print(connection)
except TypeError:
    print("Error: Failed to create Connection objects. Please check the import path or class definition.")

try:
    lines = load_lines()
    print("\nLines Loaded:")
    for line in lines:
        print(line)
except TypeError:
    print("Error: Failed to create Line objects. Please check the import path or class definition.")

try:
    shipments = load_shipments()
    print("\nShipments Loaded:")
    for shipment in shipments:
        print(shipment)
except TypeError:
    print("Error: Failed to create Shipment objects. Please check the import path or class definition.")

try:
    constants = load_constants()
    print("\nConstants Loaded:")
    for constant in constants:
        print(constant)
except TypeError:
    print("Error: Failed to create Constant objects. Please check the import path or class definition.")

# Creating a single driver manually since they are not loaded from the database
driver = Driver(driver_id=1, name='Driver A', hourly_pay=20)

# Start with one truck
def create_new_truck(truck_id, driver, constants):
    return Truck(truck_id=truck_id, driver=driver, capacity=constants[0].get_truck_capacity(), velocity=constants[0].get_velocity())

trucks = [create_new_truck(1, driver, constants)]

# Calculate the shortest distance between two locations using Dijkstra's algorithm
def dijkstra(locations, connections, start_location, target_location):
    distances = {location: float('inf') for location in locations}
    distances[start_location] = 0
    priority_queue = [(0, start_location)]
    visited = set()

    while priority_queue:
        current_distance, current_location = heapq.heappop(priority_queue)

        if current_location in visited:
            continue
        visited.add(current_location)

        if current_location == target_location:
            return current_distance

        for connection in connections:
            if connection.get_location1() == current_location:
                neighbor = connection.get_location2()
            elif connection.get_location2() == current_location:
                neighbor = connection.get_location1()
            else:
                continue

            if neighbor in visited:
                continue

            distance = current_distance + 100  # Assuming each connection represents a distance of 100 km for simplicity
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return 1000  # If no path is found, return a default distance of 1000 km to avoid skipping the shipment

# Algorithm to simulate shipments, optimizing routes and ensuring products do not expire
def simulate_shipments(trucks, shipments, constants, connections):
    today = datetime.date.today()
    used_trucks = []
    assigned_locations = set()

    # Create a list of shipments sorted by the closest expiration date of the products in them
    shipments_sorted = sorted(shipments, key=lambda s: s.get_line().get_product().get_manufacturing_time() + s.get_line().get_product().get_expiration_from_manufacturing())

    for shipment in shipments_sorted:
        location = shipment.get_location()
        product = shipment.get_line().get_product()
        expiration_date = today + datetime.timedelta(days=product.get_manufacturing_time() + product.get_expiration_from_manufacturing())
        days_until_expiration = (expiration_date - today).days

        # If the location is None, skip the shipment
        if location is None:
            print("Warning: Shipment location is None, skipping shipment.")
            continue

        # If the location has already been assigned to a truck, skip it
        if location in assigned_locations:
            continue

        # Find all shipments for the same location
        same_location_shipments = [s for s in shipments_sorted if s.get_location() == location]

        # Calculate the shortest distance to the destination using Dijkstra's algorithm
        origin = next((loc for loc in locations if loc.get_name() == 'Mataró'), None)  # Set origin to Mataró if it exists
        if origin is None:
            print("Error: Origin location 'Mataró' not found.")
            return
        print("ORIGIN:", origin)
        print("CONNECTIONS:", connections)
        print("LOCATION:", location)
        distance_to_destination = dijkstra(locations, connections, origin, location)
        velocity = constants[0].get_velocity()

        # Calculate the time needed to reach the destination
        time_needed_hours = distance_to_destination / velocity
        days_needed = time_needed_hours / constants[0].get_workday_time()  # Convert travel hours to workdays
        print(f"Distance to destination: {distance_to_destination} km, Time needed: {time_needed_hours} hours, Days needed: {days_needed} days")

        # Find a truck that can handle all shipments for this location without the product expiring
        truck_assigned = False
        total_quantity = sum(s.get_line().get_quantity() for s in same_location_shipments)

        for truck in used_trucks:
            # If the product can't reach the destination without expiring, move all products to a new truck
            if truck.get_capacity() >= total_quantity and days_until_expiration > days_needed:
                truck.get_shipments().extend(same_location_shipments)
                truck.set_capacity(truck.get_capacity() - total_quantity)
                assigned_locations.add(location)
                truck_assigned = True
                break
            elif truck.get_capacity() >= total_quantity and days_until_expiration <= days_needed:
                # Move all products of this location to a new truck if any product is at risk of expiring
                used_trucks.remove(truck)
                new_truck = create_new_truck(len(used_trucks) + 1, driver, constants)
                new_truck.set_capacity(constants[0].get_truck_capacity() - total_quantity)
                new_truck.set_shipments(same_location_shipments)
                assigned_locations.add(location)
                used_trucks.append(new_truck)
                truck_assigned = True
                break

        # If no truck is available, create a new truck and assign all shipments for this location
        if not truck_assigned:
            new_truck = create_new_truck(len(used_trucks) + 1, driver, constants)
            new_truck.set_capacity(constants[0].get_truck_capacity() - total_quantity)
            new_truck.set_shipments(same_location_shipments)
            assigned_locations.add(location)
            used_trucks.append(new_truck)

    # Print results
    for truck in used_trucks:
        print(f"Truck {truck.get_truck_id()} is used with shipments:")
        for shipment in truck.get_shipments():
            location = shipment.get_location()
            if location is None:
                print("Warning: Shipment location is None, skipping.")
                continue
            print(f"  Shipment {shipment.get_shipment_id()} with product {shipment.get_line().get_product().get_name()} to location {location.get_name()}")

        # Generate the route for each truck based on the assigned shipments
        if truck.get_shipments():
            route = [next((loc for loc in locations if loc.get_name() == 'Mataró'), None)]  # Start route from Mataró
            for shipment in truck.get_shipments():
                location = shipment.get_location()
                if location is not None and location not in route:
                    route.append(location)

            # Ensure the route starts from Mataró and then goes to other locations
            route_str = " -> ".join([loc.get_name() for loc in route if loc is not None])
            print(f"  Route: {route_str}")

    print(f"Total trucks used: {len(used_trucks)}")

# Helper function to check if two locations are nearby based on connections
def are_locations_nearby(location1, location2, connections):
    for connection in connections:
        if (connection.get_location1() == location1 and connection.get_location2() == location2) or (connection.get_location1() == location2 and connection.get_location2() == location1):
            return True
    return False

# Example usage of the simulation algorithm
simulate_shipments(trucks, shipments, constants, connections)

