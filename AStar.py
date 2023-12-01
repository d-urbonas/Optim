import heapq  # min heap by default

""" A* explanation: Similar to dijkstra's but heuristic function is used to make order which nodes to explore first 
based on their position in relation to the goal node as defined by the heuristic function (manhattan distance in our case) 
meaning the nodes that are closet as defined by the heuristic will have lower cost and therefore be explored first.
"""
def astar(graph, start, goal, nodes):
    # Priority queue to store (f_cost, node) pairs
    open_set = [(heuristic(nodes, start, goal), start)]  # start with beginning node and its heuristic cost

    # Cost and predecessors dictionaries
    g_cost = {node: float('inf') for node in graph} # current cost found so far (same a dijkstra's cost)
    g_cost[start] = 0
    predecessors = {node: None for node in graph}

    while open_set:
        # pop nodes based on f_cost
        current_f_cost, current_node = heapq.heappop(open_set)

        if current_node == goal:
            return reconstruct_path(predecessors, goal)

        for neighbor, weight in graph[current_node]:
            tentative_g_cost = g_cost[current_node] + weight
            if tentative_g_cost < g_cost[neighbor]:  # checks if new path is less weight than current path to neighbor
                g_cost[neighbor] = tentative_g_cost
                # f_cost defined by both g_cost (weight based) and heuristic cost
                f_cost = tentative_g_cost + heuristic(nodes, neighbor, goal)
                predecessors[neighbor] = current_node  # set predecessor to current to keep track of path
                heapq.heappush(open_set, (f_cost, neighbor))

    return None  # No path found

def reconstruct_path(predecessors, goal):
    path = []
    current_node = goal

    while current_node is not None:
        path.insert(0, current_node)  # Insert at the beginning to reverse the path
        current_node = predecessors[current_node]

    return path


# heuristic (Manhattan distance in this case)
def heuristic(nodes, current, goal):  # constant time function as nodes is a hashmap
    return abs(nodes[current][0] - nodes[goal][0]) + abs(nodes[current][1] - nodes[goal][1])

