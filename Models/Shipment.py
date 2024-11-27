class Shipment:
    def __init__(self, shipment_id, date, client, location, line):
        self.shipment_id = shipment_id
        self.date = date
        self.client = client
        self.location = location
        self.line = line

    def __repr__(self):
        return (f"Shipment(shipment_id={self.shipment_id}, date='{self.date}', client={self.client}, "
                f"location={self.location}, line={self.line})")

    # Getters and Setters
    def get_shipment_id(self):
        return self.shipment_id

    def set_shipment_id(self, shipment_id):
        self.shipment_id = shipment_id

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def get_client(self):
        return self.client

    def set_client(self, client):
        self.client = client

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location

    def get_line(self):
        return self.line

    def set_line(self, line):
        self.line_= line