from dijkstra import dijkstra
from truck_operations import create_new_truck, assign_shipments_to_truck
import datetime

# Simulate shipments, optimizing routes and ensuring products do not expire
def simulate_shipments(trucks, shipments, constants, connections, locations, driver):
    today = datetime.date.today()
    used_trucks = []
    assigned_locations = set()
    truck_routes = []

    # Create a list of shipments sorted by the closest expiration date of the products in them
    shipments_sorted = sorted(shipments, key=lambda s: s.get_line().get_product().get_manufacturing_time() + s.get_line().get_product().get_expiration_from_manufacturing())

    for shipment in shipments_sorted:
        location = shipment.get_location()
        product = shipment.get_line().get_product()
        expiration_date = today + datetime.timedelta(days=product.get_manufacturing_time() + product.get_expiration_from_manufacturing())
        days_until_expiration = (expiration_date - today).days

        # Skip shipment if location is None
        if location is None:
            print("Warning: Shipment location is None, skipping shipment.")
            continue

        # Skip if location already assigned to a truck
        if location in assigned_locations:
            continue

        # Find all shipments for the same location
        same_location_shipments = [s for s in shipments_sorted if s.get_location() == location]

        # Set origin to either the last assigned location or Mataró
        if used_trucks:
            last_location = used_trucks[-1].get_shipments()[-1].get_location() if used_trucks[-1].get_shipments() else None
        else:
            last_location = next((loc for loc in locations if loc.get_name() == 'Mataró'), None)

        if last_location is None:
            print("Error: Starting location 'Mataró' not found.")
            return

        # Calculate shortest distance to the destination
        distance_to_destination = dijkstra(locations, connections, last_location.get_name(), location.get_name())
        velocity = constants[0].get_velocity()

        # Calculate time needed to reach the destination
        time_needed_hours = distance_to_destination / velocity
        days_needed = time_needed_hours / constants[0].get_workday_time()

        # Check if the shipment can be delivered before product expiration
        if days_needed > days_until_expiration:
            print(f"Warning: Shipment {shipment.get_shipment_id()} with product {product.get_name()} cannot reach destination on time. Skipping shipment.", 
                  f"Days needed:{days_needed}, days_until_expiration:{days_until_expiration}")
            continue

        # Assign the shipments to a truck
        truck_assigned = False
        total_quantity = sum(s.get_line().get_quantity() for s in same_location_shipments)

        for truck in used_trucks:
            if truck.get_capacity() >= total_quantity:
                assign_shipments_to_truck(truck, same_location_shipments)
                assigned_locations.add(location)
                truck_assigned = True
                break

        # If no truck is available, create a new truck and assign shipments
        if not truck_assigned:
            new_truck = create_new_truck(len(used_trucks) + 1, driver, constants)
            assign_shipments_to_truck(new_truck, same_location_shipments)
            assigned_locations.add(location)
            used_trucks.append(new_truck)

    # Generate and print routes for each truck
    for truck in used_trucks:
        print(f"Truck {truck.get_truck_id()} is used with shipments:")
        route = []

        for shipment in truck.get_shipments():
            location = shipment.get_location()
            if location is None:
                print("Warning: Shipment location is None, skipping.")
                continue
            print(f"  Shipment {shipment.get_shipment_id()} with product {shipment.get_line().get_product().get_name()} to location {location.get_name()}")
            if location not in route:
                route.append(location)

        # Ensure the route starts from Mataró and then goes to other locations
        origin_location = next((loc for loc in locations if loc.get_name() == 'Mataró'), None)
        if origin_location is not None:
            route.insert(0, origin_location)

        route_str = " -> ".join([loc.get_name() for loc in route if loc is not None])
        print(f"  Route: {route_str}")

        # Store the route
        truck_routes.append({
            "truck_id": truck.get_truck_id(),
            "route": route_str
        })

    print(f"Total trucks used: {len(used_trucks)}")

    # Return the truck routes
    return truck_routes
