import sqlite3

# Conectar a la base de datos (se creará si no existe)
conn = sqlite3.connect('logistics_project.db')
cursor = conn.cursor()

# Crear tabla Locations
cursor.execute('''
CREATE TABLE IF NOT EXISTS Locations (
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
)
''')

# Crear tabla Connections
cursor.execute('''
CREATE TABLE IF NOT EXISTS Connections (
    connection_id INTEGER PRIMARY KEY AUTOINCREMENT,
    location1 INTEGER NOT NULL,
    location2 INTEGER NOT NULL,
    FOREIGN KEY (location1) REFERENCES Locations(location_id),
    FOREIGN KEY (location2) REFERENCES Locations(location_id)
)
''')

# Crear tabla Products
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    manufacturing_time INTEGER NOT NULL,
    expiration_from_manufacturing INTEGER NOT NULL
)
''')

# Crear tabla Lines
cursor.execute('''
CREATE TABLE IF NOT EXISTS Lines (
    line_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
)
''')

# Crear tabla Clients
cursor.execute('''
CREATE TABLE IF NOT EXISTS Clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
''')

# Crear tabla Shipments
cursor.execute('''
CREATE TABLE IF NOT EXISTS Shipments (
    shipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    client_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    line_id INTEGER NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id),
    FOREIGN KEY (location_id) REFERENCES Locations(location_id),
    FOREIGN KEY (line_id) REFERENCES Lines(line_id)
)
''')

# Crear tabla Constants
cursor.execute('''
CREATE TABLE IF NOT EXISTS Constants (
    constant_id INTEGER PRIMARY KEY AUTOINCREMENT,
    velocity REAL NOT NULL,
    workday_time INTEGER NOT NULL,
    rest_time INTEGER NOT NULL,
    drivers_hourly_pay REAL NOT NULL,
    fuel_cost_km REAL NOT NULL,
    truck_capacity INTEGER NOT NULL
)
''')

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()

print("Las tablas se han creado correctamente.")
