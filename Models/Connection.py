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
