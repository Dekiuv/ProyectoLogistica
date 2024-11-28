import heapq

# Dijkstra's algorithm to calculate the shortest distance between two locations
def dijkstra(locations, connections, start_location_name, target_location_name):
    # Convert `start_location_name` and `target_location_name` to `Location` objects
    start_location = next((loc for loc in locations if loc.get_name() == start_location_name), None)
    target_location = next((loc for loc in locations if loc.get_name() == target_location_name), None)
    
    if not start_location or not target_location:
        print("Error: One or both locations not found.")
        return float('inf')

    # Initialize distances with infinity, set the start location distance to 0
    distances = {location.get_location_id(): float('inf') for location in locations}
    distances[start_location.get_location_id()] = 0
    priority_queue = [(0, start_location)]
    visited = set()

    while priority_queue:
        current_distance, current_location = heapq.heappop(priority_queue)

        # If the current location has been visited, skip it
        if current_location.get_location_id() in visited:
            continue
        visited.add(current_location.get_location_id())

        # If we have reached the target location, return the current distance
        if current_location.get_location_id() == target_location.get_location_id():
            return current_distance

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

            # Calculate distance to the neighbor and update if it is smaller
            distance = current_distance + connection.get_distance()
            print("Distance: ", current_location, neighbor)
            if distance < distances[neighbor.get_location_id()]:
                distances[neighbor.get_location_id()] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    # If no path is found, return infinity
    return float('inf')
