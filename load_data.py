from load_db_data import *

def load_all_data():
    try:
        locations = load_locations()
        # print("Locations Loaded:")
        # for location in locations:
            # print(location)
    except TypeError:
        print("Error: Failed to create Location objects. Please check the import path or class definition.")
        locations = []

    try:
        products = load_products()
        # print("\nProducts Loaded:")
        # for product in products:
            # print(product)
    except TypeError:
        print("Error: Failed to create Product objects. Please check the import path or class definition.")
        products = []

    try:
        clients = load_clients()
        # print("\nClients Loaded:")
        # for client in clients:
            # print(client)
    except TypeError:
        print("Error: Failed to create Client objects. Please check the import path or class definition.")
        clients = []

    try:
        connections = load_connections()
        # print("\nConnections Loaded:")
        # for connection in connections:
            # print(connection)
    except TypeError:
        print("Error: Failed to create Connection objects. Please check the import path or class definition.")
        connections = []

    try:
        lines = load_lines()
        # print("\nLines Loaded:")
        # for line in lines:
            # print(line)
    except TypeError:
        print("Error: Failed to create Line objects. Please check the import path or class definition.")
        lines = []

    try:
        shipments = load_shipments()
        # print("\nShipments Loaded:")
        # for shipment in shipments:
            # print(shipment)
    except TypeError:
        print("Error: Failed to create Shipment objects. Please check the import path or class definition.")
        shipments = []

    try:
        constants = load_constants()
        # print("\nConstants Loaded:")
        # for constant in constants:
            # print(constant)
    except TypeError:
        print("Error: Failed to create Constant objects. Please check the import path or class definition.")
        constants = []

    return locations, products, clients, connections, lines, shipments
