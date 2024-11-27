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

# Algorithm to simulate shipments, optimizing routes and ensuring products do not expire
def simulate_shipments(trucks, shipments, constants):
    today = datetime.date.today()
    used_trucks = []

    # Create a list of shipments sorted by the closest expiration date of the products in them
    shipments_sorted = sorted(shipments, key=lambda s: s.get_line().get_product().get_manufacturing_time() + s.get_line().get_product().get_expiration_from_manufacturing())

    for shipment in shipments_sorted:
        product = shipment.get_line().get_product()
        expiration_date = today + datetime.timedelta(days=product.get_manufacturing_time() + product.get_expiration_from_manufacturing())
        days_until_expiration = (expiration_date - today).days

        # Find a truck that can handle the shipment without the product expiring
        truck_assigned = False
        for truck in used_trucks:
            if truck.get_capacity() > 0 and days_until_expiration > 0:
                truck.get_shipments().append(shipment)
                truck.set_capacity(truck.get_capacity() - shipment.get_line().get_quantity())
                truck_assigned = True
                break

        # If no truck is available, create a new truck and assign the shipment
        if not truck_assigned:
            new_truck = create_new_truck(len(used_trucks) + 1, driver, constants)
            new_truck.set_capacity(constants[0].get_truck_capacity() - shipment.get_line().get_quantity())
            new_truck.set_shipments([shipment])
            used_trucks.append(new_truck)

    # Print results
    for truck in used_trucks:
        print(f"Truck {truck.get_truck_id()} is used with shipments:")
        for shipment in truck.get_shipments():
            location = shipment.get_location()
            if location:
                print(f"  Shipment {shipment.get_shipment_id()} with product {shipment.get_line().get_product().get_name()} to location {location.get_name()}")

        # Generate the route for each truck based on the assigned shipments
        if truck.get_shipments():
            route = []
            for shipment in truck.get_shipments():
                location = shipment.get_location()
                if location and location not in route:
                    route.append(location)

            # Print the route for the truck
            route_str = " -> ".join([loc.get_name() for loc in route])
            print(f"  Route: {route_str}")

    print(f"Total trucks used: {len(used_trucks)}")

# Example usage of the simulation algorithm
simulate_shipments(trucks, shipments, constants)
