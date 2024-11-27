class Location:
    def __init__(self, location_id, name, latitude, longitude):
        self.location_id = location_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Location(location_id={self.location_id}, name='{self.name}', latitude={self.latitude}, longitude={self.longitude})"

    # Getters and Setters
    def get_location_id(self):
        return self.location_id

    def set_location_id(self, location_id):
        self.location_id = location_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_latitude(self):
        return self.latitude

    def set_latitude(self, latitude):
        self.latitude = latitude

    def get_longitude(self):
        return self.longitude

    def set_longitude(self, longitude):
        self.longitude = longitude