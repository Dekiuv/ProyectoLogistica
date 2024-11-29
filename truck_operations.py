from Models.Truck import Truck
from Models.Driver import Driver
import random
# Global variable to keep track of the last driver created
last_driver_id = 'A'

# Function to automatically create the next Driver instance
def create_next_driver(base_name="Driver", base_hourly_pay=20):
    global last_driver_id
    
    # Get the next letter in the sequence
    driver_id = chr(ord(last_driver_id) + 1)
    driver_id2 = chr(ord(last_driver_id) + 5)
    
    # Create driver instance
    name = f"{base_name} {driver_id}.{driver_id2}"  # e.g., 'Driver B', 'Driver C', etc.
    hourly_pay = base_hourly_pay + random.uniform(-5, 5)  # Randomly vary hourly pay within ±5
    
    # Update last driver id to the current one
    last_driver_id = driver_id
    
    driver = Driver(driver_id=driver_id, name=name, hourly_pay=hourly_pay)
    
    return driver


def create_new_truck(truck_id, driver, constants):
    return Truck(truck_id=truck_id, driver=driver, capacity=constants[0].get_truck_capacity(), velocity=constants[0].get_velocity())

def assign_shipments_to_truck(truck, shipments):
    truck.get_shipments().extend(shipments)
    total_quantity = sum(s.get_line().get_quantity() for s in shipments)
    truck.set_capacity(truck.get_capacity() - total_quantity)
    return truck
