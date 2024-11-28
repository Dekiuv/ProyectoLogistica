from Models.Truck import Truck

def create_new_truck(truck_id, driver, constants):
    return Truck(truck_id=truck_id, driver=driver, capacity=constants[0].get_truck_capacity(), velocity=constants[0].get_velocity())

def assign_shipments_to_truck(truck, shipments):
    truck.get_shipments().extend(shipments)
    total_quantity = sum(s.get_line().get_quantity() for s in shipments)
    truck.set_capacity(truck.get_capacity() - total_quantity)
    return truck
