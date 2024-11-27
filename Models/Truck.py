class Truck:
    def __init__(self, truck_id, driver, capacity, velocity):
        self.truck_id = truck_id
        self.driver = driver
        self.capacity = capacity
        self.velocity = velocity
        self.shipments = []

    def __repr__(self):
        return (f"Truck(truck_id={self.truck_id}, driver={self.driver}, capacity={self.capacity}, "
                f"velocity={self.velocity})")

    # Getters and Setters
    def get_truck_id(self):
        return self.truck_id

    def set_truck_id(self, truck_id):
        self.truck_id = truck_id

    def get_driver(self):
        return self.driver

    def set_driver(self, driver):
        self.driver = driver

    def get_capacity(self):
        return self.capacity

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

    def get_shipments(self):
        return self.shipments

    def set_shipments(self, shipments):
        self.shipments = shipments
