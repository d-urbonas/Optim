import heapq

def dijkstra(graph, start, end):
    # Initialize distances and predecessors
    distances = {node: float('infinity') for node in graph}
    predecessors = {node: None for node in graph}
    distances[start] = 0

    # Priority queue to store (distance, node) pairs
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Check if the current distance is already greater than the known distance
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            # If a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, predecessors

def get_shortest_path(predecessors, start, end):
    path = []
    current_node = end

    while current_node is not None:
        path.insert(0, current_node)  # Insert at the beginning to reverse the path
        current_node = predecessors[current_node]

    if path[0] == start:
        return path
    else:
        return []  # No path found