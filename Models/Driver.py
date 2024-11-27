class Driver:
    def __init__(self, driver_id, name, hourly_pay):
        self.driver_id = driver_id
        self.name = name
        self.hourly_pay = hourly_pay

    def __repr__(self):
        return f"Driver(driver_id={self.driver_id}, name='{self.name}', hourly_pay={self.hourly_pay})"

    # Getters and Setters
    def get_driver_id(self):
        return self.driver_id

    def set_driver_id(self, driver_id):
        self.driver_id = driver_id

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_hourly_pay(self):
        return self.hourly_pay

    def set_hourly_pay(self, hourly_pay):
        self.hourly_pay = hourly_pay
