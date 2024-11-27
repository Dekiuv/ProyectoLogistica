import sqlite3
from Models.Location import Location
from Models.Connection import Connection
from Models.Product import Product
from Models.Line import Line
from Models.Client import Client
from Models.Shipment import Shipment
from Models.Constant import Constant
from Models.Driver import Driver
from Models.Truck import Truck

def load_locations():
    conn = sqlite3.connect('logistics_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Locations")
    locations = [Location(location_id=row[0], name=row[1], latitude=row[2], longitude=row[3]) for row in cursor.fetchall()]
    conn.close()
    return locations

def load_connections():
    locations = load_locations()
    location_dict = {location.location_id: location for location in locations}

    conn = sqlite3.connect('logistics_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Connections")
    connections = [
        Connection(connection_id=row[0], location1=location_dict.get(row[1]), location2=location_dict.get(row[2]))
        for row in cursor.fetchall()
    ]
    conn.close()
    return connections

def load_products():
    conn = sqlite3.connect('logistics_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products")
    products = [Product(product_id=row[0], name=row[1], price=row[2], manufacturing_time=row[3], expiration_from_manufacturing=row[4]) for row in cursor.fetchall()]
    conn.close()
    return products

def load_lines():
    products = load_products()
    product_dict = {product.product_id: product for product in products}

    conn = sqlite3.connect('logistics_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Lines")
    line_rows = cursor.fetchall()
    conn.close()

    lines = []
    for row in line_rows:
        product = product_dict.get(row[1])
        if product:
            line = Line(line_id=row[0], product=product, quantity=row[2])
            lines.append(line)
    return lines

def load_clients():
    conn = sqlite3.connect('logistics_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Clients")
    clients = [Client(client_id=row[0], name=row[1]) for row in cursor.fetchall()]
    conn.close()
    return clients

def load_shipments():
    clients = load_clients()
    locations = load_locations()
    lines = load_lines()

    client_dict = {client.client_id: client for client in clients}
    location_dict = {location.location_id: location for location in locations}
    line_dict = {line.line_id: line for line in lines}

    conn = sqlite3.connect('logistics_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Shipments")
    shipments = [
        Shipment(
            shipment_id=row[0],
            date=row[1],
            client=client_dict.get(row[2]),
            location=location_dict.get(row[3]),
            line=line_dict.get(row[4])
        )
        for row in cursor.fetchall()
    ]
    conn.close()
    return shipments

def load_constants():
    conn = sqlite3.connect('logistics_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Constants")
    constants = [Constant(constant_id=row[0], velocity=row[1], workday_time=row[2], rest_time=row[3], drivers_hourly_pay=row[4], fuel_cost_km=row[5], truck_capacity=row[6]) for row in cursor.fetchall()]
    conn.close()
    return constants
