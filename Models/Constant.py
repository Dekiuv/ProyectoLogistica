class Constant:
    def __init__(self, constant_id, velocity, workday_time, rest_time, drivers_hourly_pay, fuel_cost_km, truck_capacity):
        # Asegurar que todos los valores tienen el tipo correcto
        self.constant_id = int(constant_id)
        self.velocity = float(velocity)
        self.workday_time = float(workday_time)
        self.rest_time = float(rest_time)
        self.drivers_hourly_pay = float(drivers_hourly_pay)
        self.fuel_cost_km = float(fuel_cost_km)
        self.truck_capacity = float(truck_capacity)

    def __repr__(self):
        return (f"Constant(constant_id={self.constant_id}, velocity={self.velocity}, workday_time={self.workday_time}, "
                f"rest_time={self.rest_time}, drivers_hourly_pay={self.drivers_hourly_pay}, fuel_cost_km={self.fuel_cost_km}, "
                f"truck_capacity={self.truck_capacity})")

    # Getters and Setters
    def get_constant_id(self):
        return self.constant_id

    def set_constant_id(self, constant_id):
        self.constant_id = int(constant_id)

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = float(velocity)

    def get_workday_time(self):
        return self.workday_time

    def set_workday_time(self, workday_time):
        self.workday_time = float(workday_time)

    def get_rest_time(self):
        return self.rest_time

    def set_rest_time(self, rest_time):
        self.rest_time = float(rest_time)

    def get_drivers_hourly_pay(self):
        return self.drivers_hourly_pay

    def set_drivers_hourly_pay(self, drivers_hourly_pay):
        self.drivers_hourly_pay = float(drivers_hourly_pay)

    def get_fuel_cost_km(self):
        return self.fuel_cost_km

    def set_fuel_cost_km(self, fuel_cost_km):
        self.fuel_cost_km = float(fuel_cost_km)

    def get_truck_capacity(self):
        return self.truck_capacity

    def set_truck_capacity(self, truck_capacity):
        self.truck_capacity = float(truck_capacity)
