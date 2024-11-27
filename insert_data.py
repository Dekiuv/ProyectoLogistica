import sqlite3
import csv
from conexiones import provincias_espana

# Conectar a la base de datos SQLite
conn = sqlite3.connect('logistics_project.db')
cursor = conn.cursor()

#INSERTAR LOCALIZACIONES

#UBICACIONES

# Abrir el archivo CSV
with open('Ubicacion.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Para saltar la primera línea de cabecera

    # Insertar los datos en la tabla Locations
    for row in reader:
        provincia = row[1]  # Provincia
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
with open('clientes.csv', newline='', encoding='utf-8') as csvfile:
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
with open('products.csv', newline='', encoding='utf-8') as csvfile:
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
with open('lines.csv', newline='', encoding='utf-8') as csvfile:
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
with open('shipments.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Para saltar la primera línea de cabecera

    # Insertar los datos en la tabla Locations
    for row in reader:
        shipment_id = row[0]
        date = row[1]
        client_id = row[2]
        location_id = row[3]
        line_id = row[4]

        # Insertar los datos en la tabla Locations
        cursor.execute('''
            INSERT INTO Shipments (shipment_id, date, client_id, location_id, line_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (shipment_id, date, client_id, location_id, line_id))

# Confirmar los cambios
conn.commit()

print("Datos insertados correctamente en la tabla Products.")

# CONSTANTS

# Abrir el archivo CSV
with open('constants.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Para saltar la primera línea de cabecera

    # Insertar los datos en la tabla Locations
    for row in reader:
        constant_id = row[0]
        velocity = row[1]
        workday_time = row[2]
        rest_time = row[3]
        drivers_hourly_pay = row[4]
        fuel_cost_km = row[5]
        truck_capacity = row[6]

        # Insertar los datos en la tabla Locations
        cursor.execute('''
            INSERT INTO Constants (constant_id, velocity, workday_time, rest_time, drivers_hourly_pay, fuel_cost_km, truck_capacity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (constant_id, velocity, workday_time, rest_time, drivers_hourly_pay, fuel_cost_km, truck_capacity))

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