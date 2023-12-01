import heapq

def astar(graph, start, goal, nodes):
    # Priority queue to store (f_cost, node) pairs
    open_set = [(0 + heuristic(nodes, start, goal), start)]

    # Cost and predecessors dictionaries
    g_cost = {node: float('infinity') for node in graph}
    g_cost[start] = 0
    predecessors = {node: None for node in graph}

    while open_set:
        current_f_cost, current_node = heapq.heappop(open_set)

        if current_node == goal:
            return reconstruct_path(predecessors, start, goal)

        for neighbor, weight in graph[current_node]:
            tentative_g_cost = g_cost[current_node] + weight
            if tentative_g_cost < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g_cost
                f_cost = tentative_g_cost + heuristic(nodes, neighbor, goal)
                predecessors[neighbor] = current_node
                heapq.heappush(open_set, (f_cost, neighbor))

    return None  # No path found

def reconstruct_path(predecessors, start, goal):
    path = []
    current_node = goal

    while current_node is not None:
        path.insert(0, current_node)  # Insert at the beginning to reverse the path
        current_node = predecessors[current_node]

    return path


# heuristic (Manhattan distance in this case)
def heuristic(nodes, current, goal):
    return abs(nodes[current][0] - nodes[goal][0]) + abs(nodes[current][1] - nodes[goal][1])

