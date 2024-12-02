from Models.Truck import Truck
from Models.Driver import Driver
import random
# Global variable to keep track of the last driver created
last_driver_id = 'A'

# Function to automatically create the next Driver instance
def create_next_driver(base_name="Driver", base_hourly_pay=20):
    global last_driver_id

    # Asegurarse de que solo se utilizan letras del alfabeto
    if last_driver_id > 'Z':
        last_driver_id = 'A'  # Reiniciar al principio si excedemos 'Z'

    # Obtener la siguiente letra en la secuencia
    driver_id = last_driver_id

    # Crear instancia de Driver con un nombre secuencial basado en letras
    name = f"{base_name} {driver_id}"  # e.g., 'Driver A', 'Driver B', etc.
    hourly_pay = base_hourly_pay + random.uniform(-5, 5)  # Varia el salario dentro de ±5

    # Actualizar el último id de conductor al siguiente carácter en la secuencia alfabética
    last_driver_id = chr(ord(last_driver_id) + 1)  # Avanzar a la siguiente letra del alfabeto

    driver = Driver(driver_id=driver_id, name=name, hourly_pay=hourly_pay)
    
    return driver


def create_new_truck(truck_id, driver, constants):
    return Truck(truck_id=truck_id, driver=driver, capacity=constants[0].get_truck_capacity(), velocity=constants[0].get_velocity())

def assign_shipments_to_truck(truck, shipments):
    truck.get_shipments().extend(shipments)
    total_quantity = sum(s.get_line().get_quantity() for s in shipments)
    truck.set_capacity(truck.get_capacity() - total_quantity)
    return truck
