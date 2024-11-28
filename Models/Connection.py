import math

class Connection:
    def __init__(self, connection_id, location1, location2):
        self.connection_id = connection_id
        self.location1 = location1
        self.location2 = location2

    def __repr__(self):
        return f"Connection(connection_id={self.connection_id}, location1={self.location1}, location2={self.location2})"

    # Getters and Setters
    def get_connection_id(self):
        return self.connection_id

    def set_connection_id(self, connection_id):
        self.connection_id = connection_id

    def get_location1(self):
        return self.location1

    def set_location1(self, location1):
        self.location1 = location1

    def get_location2(self):
        return self.location2

    def set_location2(self, location2):
        self.location2 = location2

    # Método para obtener la distancia entre las dos ubicaciones
    def get_distance(self):
        lat1, lon1 = self.location1.get_latitude(), self.location1.get_longitude()
        lat2, lon2 = self.location2.get_latitude(), self.location2.get_longitude()

        # Calcular la distancia usando la fórmula de Haversine
        radius = 6371  # Radio de la Tierra en km

        # Convertir latitudes y longitudes de grados a radianes
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        # Fórmula de Haversine
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = radius * c
        return distance
