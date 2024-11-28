from load_data import load_all_data
from simulation import simulate_shipments_with_clustering
from truck_operations import create_new_truck
from Models.Driver import Driver
from dijkstra import dijkstra

# Load data
locations, products, clients, connections, lines, shipments, constants = load_all_data()

# Create a driver manually since it is not loaded from the database
driver = Driver(driver_id=1, name='Driver A', hourly_pay=20)

# Start with one truck
trucks = [create_new_truck(1, driver, constants)]

# Run the simulation
routes = simulate_shipments_with_clustering(trucks, shipments, constants, connections, locations, driver)

print