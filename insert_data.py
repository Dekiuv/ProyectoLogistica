import sqlite3
import csv
from conexiones import provincias_espana

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


# Conectar a la base de datos SQLite
conn = sqlite3.connect('logistics_project.db')
cursor = conn.cursor()

#INSERTAR LOCALIZACIONES

#UBICACIONES

# Abrir el archivo CSV
with open('./Data/Ubicacion.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Para saltar la primera línea de cabecera

    # Insertar los datos en la tabla Locations
    for row in reader:
        provincia = row[0]  # Provincia
        latitud = row[2].replace(',', '.')  # Reemplazar la coma por punto para el formato decimal
        longitud = row[3].replace(',', '.')  # Reemplazar la coma por punto para el formato decimal

        # Insertar los datos en la tabla Locations
        cursor.execute('''
            INSERT INTO Locations (name, latitude, longitude)
            VALUES (?, ?, ?)
        ''', (provincia, latitud, longitud))

# Confirmar los cambios
conn.commit()

print("Datos insertados correctamente en la tabla Locations.")

# CLIENTES

# Abrir el archivo CSV
with open('./Data/clientes.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Para saltar la primera línea de cabecera

    # Insertar los datos en la tabla Locations
    for row in reader:
        client_id = row[0] # Reemplazar la coma por punto para el formato decimal
        name = row[1]  # Reemplazar la coma por punto para el formato decimal

        # Insertar los datos en la tabla Locations
        cursor.execute('''
            INSERT INTO Clients (client_id, name)
            VALUES (?, ?)
        ''', (client_id, name))

# Confirmar los cambios
conn.commit()

print("Datos insertados correctamente en la tabla Clients.")


# PRODUCTO

# Abrir el archivo CSV
with open('./Data/products.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Para saltar la primera línea de cabecera

    # Insertar los datos en la tabla Locations
    for row in reader:
        product_id = row[0]
        name = row[1]
        price = row[2].replace(',', '.')
        manufacturing_time = row[3]
        expiration_from_manufacturing = row[4]

        # Insertar los datos en la tabla Locations
        cursor.execute('''
            INSERT INTO Products (product_id, name, price, manufacturing_time, expiration_from_manufacturing)
            VALUES (?, ?, ?, ?, ?)
        ''', (product_id, name, price, manufacturing_time, expiration_from_manufacturing))

# Confirmar los cambios
conn.commit()

print("Datos insertados correctamente en la tabla Products.")
# LINES

# Abrir el archivo CSV
with open('./Data/lines.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Para saltar la primera línea de cabecera

    # Insertar los datos en la tabla Locations
    for row in reader:
        line_id = row[0]
        product_id = row[1]
        quantity = row[2]

        # Insertar los datos en la tabla Locations
        cursor.execute('''
            INSERT INTO Lines (line_id, product_id, quantity)
            VALUES (?, ?, ?)
        ''', (line_id, product_id, quantity))

# Confirmar los cambios
conn.commit()

print("Datos insertados correctamente en la tabla Lines.")

# SHIPMENTS

# Abrir el archivo CSV
with open('./Data/shipments.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Para saltar la primera línea de cabecera

    # Insertar los datos en la tabla Shipments
    for row in reader:
        shipment_id = row[0]
        date = row[1]
        client_id = row[2]
        location_id = row[3]
        line_id = row[4]

        # Consultar el nombre de la ubicación a partir del location_id
        cursor.execute('SELECT name FROM Locations WHERE location_id = ?', (location_id,))
        location_name = cursor.fetchone()

        # Verificar si la ubicación no es "Mataró" antes de insertar
        if location_name and location_name[0] != "Mataró":
            cursor.execute('''
                INSERT INTO Shipments (shipment_id, date, client_id, location_id, line_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (shipment_id, date, client_id, location_id, line_id))

# Confirmar los cambios
conn.commit()


# CONSTANTS

# INSERTAR CONSTANTES EN LA TABLA Constants
# cursor.execute('''
# INSERT INTO Constants (velocity, workday_time, rest_time, drivers_hourly_pay, fuel_cost_km, truck_capacity)
# VALUES (?, ?, ?, ?, ?, ?)''',
# (80.5, 8, 1, 15.75, 1.20, 5000))

# Abrir el archivo CSV
with open('./Data/constants.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Para saltar la primera línea de cabecera

    # Insertar los datos en la tabla Locations
    for row in reader:
        # constant_id = row[0]
        velocity = row[1]
        workday_time = row[2]
        rest_time = row[3]
        drivers_hourly_pay = row[4]
        fuel_cost_km = row[5]
        truck_capacity = row[6]

        # Insertar los datos en la tabla Locations
        cursor.execute('''
            INSERT INTO Constants (velocity, workday_time, rest_time, drivers_hourly_pay, fuel_cost_km, truck_capacity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (velocity, workday_time, rest_time, drivers_hourly_pay, fuel_cost_km, truck_capacity))

# Confirmar los cambios
conn.commit()

print("Datos insertados correctamente en la tabla Products.")

#INSERTAR CONEXIONES

# Función para obtener el location_id de una provincia por su nombre
def get_location_id(provincia_name):
    cursor.execute("SELECT location_id FROM Locations WHERE name = ?", (provincia_name,))
    result = cursor.fetchone()
    return result[0] if result else None

# Insertar conexiones entre provincias
for provincia, conexiones in provincias_espana.items():
    # Obtener el id de la provincia actual
    location1_id = get_location_id(provincia)

    # Si encontramos la provincia en la base de datos
    if location1_id:
        for conexion in conexiones:
            # Obtener el id de la provincia conectada
            location2_id = get_location_id(conexion)

            # Si encontramos la provincia conectada
            if location2_id:
                # Insertar la conexión entre las dos provincias
                cursor.execute('''
                    INSERT INTO Connections (location1, location2)
                    VALUES (?, ?)
                ''', (location1_id, location2_id))

# Confirmar los cambios
conn.commit()

# Cerrar la conexión
conn.close()

print("Conexiones insertadas correctamente.")