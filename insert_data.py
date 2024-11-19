import sqlite3
import csv
from conexiones import provincias_espana

# Conectar a la base de datos SQLite
conn = sqlite3.connect('logistics_project.db')
cursor = conn.cursor()

#INSERTAR LOCALIZACIONES

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

# Cerrar la conexión
# conn.close()

print("Datos insertados correctamente en la tabla Locations.")

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