import heapq

# Dijkstra's algorithm to calculate the shortest distance and total travel time between two locations
def dijkstra(locations, connections, start_location_name, target_location_name, average_speed, workday_time, rest_time):
    # Convert `start_location_name` and `target_location_name` to `Location` objects
    start_location = next((loc for loc in locations if loc.get_name() == start_location_name), None)
    target_location = next((loc for loc in locations if loc.get_name() == target_location_name), None)
    
    if not start_location or not target_location:
        print("Error: One or both locations not found.")
        return float('inf'), float('inf'), []

    # Initialize distances and travel times with infinity, set the start location values to 0
    distances = {location.get_location_id(): float('inf') for location in locations}
    travel_times = {location.get_location_id(): float('inf') for location in locations}
    distances[start_location.get_location_id()] = 0
    travel_times[start_location.get_location_id()] = 0

    priority_queue = [(0, 0, start_location)]  # (travel_time, distance, location)
    visited = set()
    previous_nodes = {location.get_location_id(): None for location in locations}

    while priority_queue:
        current_time, current_distance, current_location = heapq.heappop(priority_queue)

        # If the current location has been visited, skip it
        if current_location.get_location_id() in visited:
            continue
        visited.add(current_location.get_location_id())

        # If we have reached the target location, return the current distance and time
        if current_location.get_location_id() == target_location.get_location_id():
            # Construct the path
            path = []
            node = target_location
            while node is not None:
                path.insert(0, node)
                node = previous_nodes[node.get_location_id()]

            # Return the total travel time, distance, and path as an array of `Location` objects
            return current_time, current_distance, path

        # Iterate over all connections to find neighbors
        for connection in connections:
            if connection.get_location1().get_location_id() == current_location.get_location_id():
                neighbor = connection.get_location2()
            elif connection.get_location2().get_location_id() == current_location.get_location_id():
                neighbor = connection.get_location1()
            else:
                continue
            
            # Skip if neighbor has been visited
            if neighbor.get_location_id() in visited:
                continue

            # Calculate distance to the neighbor
            travel_distance = connection.get_distance()
            travel_time_hours = travel_distance / average_speed

            # Calculate rest time if the travel time exceeds workday hours
            num_rest_periods = int(travel_time_hours / workday_time)
            total_rest_time = num_rest_periods * rest_time

            # Calculate the total travel time and distance
            effective_time = travel_time_hours + total_rest_time
            new_distance = current_distance + travel_distance
            new_time = current_time + effective_time

            # Update distance and time if this path is shorter
            if new_time < travel_times[neighbor.get_location_id()]:
                distances[neighbor.get_location_id()] = new_distance
                travel_times[neighbor.get_location_id()] = new_time
                previous_nodes[neighbor.get_location_id()] = current_location
                heapq.heappush(priority_queue, (new_time, new_distance, neighbor))

    # If no path is found, print and return infinity
    print("No path found. Returning infinity.")
    return float('inf'), float('inf'), []

