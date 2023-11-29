import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from Dijkstra import dijkstra
matplotlib.use('TkAgg')  # Use the TkAgg backend


def read_nodes(file_path):
    nodes = {}
    with open(file_path, 'r') as file:
        for line in file:
            node_id, longitude, latitude = map(float, line.strip().split())
            nodes[node_id] = (longitude, latitude)

    return nodes

def read_edges(file_path, max_lines=180000):
    adjacency_list = {}
    edges = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line_num > max_lines:
                break
            edgeID, node1, node2, weight = map(float, line.strip().split())

            # Convert node1 and node2 to integers
            node1 = int(node1)
            node2 = int(node2)

            edges.append((node1, node2, {'distance': weight}))
            if node1 not in adjacency_list:
                adjacency_list[node1] = []
            if node2 not in adjacency_list:
                adjacency_list[node2] = []
            adjacency_list[node1].append((node2, weight))

    return edges, adjacency_list


def create_graph(nodes, edges):
    G = nx.Graph()

    # Add nodes with positions
    for node_id, pos in nodes.items():
        G.add_node(node_id, pos=pos)

    # Add edges with attributes
    G.add_edges_from(edges)

    return G

def draw_graph(G, path_edges=None):
    node_positions = nx.get_node_attributes(G, 'pos')
    fig, ax = plt.subplots(figsize=(10, 7))  # Adjust the size as needed

    # Draw the graph
    nx.draw_networkx(G, node_positions, with_labels=False, node_size=1, node_color='skyblue', font_size=6, font_color='black', edge_color='gray', ax=ax)

    # Highlight the shortest path
    if path_edges:
        nx.draw_networkx_edges(G, edgelist=path_edges, edge_color='red', width=2, pos=node_positions)  # Include pos=node_positions

    plt.show()

def color_path(G, path):
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    return path_edges

def main():
    # File paths
    nodes_file = './input/all_edges.txt'
    edges_file = './input/edges.txt'

    # Read nodes and edges from files
    nodes = read_nodes(nodes_file)
    edges, adjacencyList = read_edges(edges_file)

    # Create graph
    graph = create_graph(nodes, edges)

    distances, predecessors = dijkstra(adjacencyList, 0)
    for node in adjacencyList:
        path = []
        current_node = node
        while current_node is not None:
            path.insert(0, current_node)
            current_node = predecessors[current_node]
        if node == 1240.0:
            print(f"Shortest path from 0 to {node}: {path}, Distance: {distances[node]}")
            path_edges = color_path(graph, path)
            break

        # Call color_path to get the edges to highlight


    # Draw the graph with the highlighted path
    draw_graph(graph, path_edges)

    #dijkstra(edges)

    # graph = {
    #     'A': {'B': 1, 'C': 4},
    #     'B': {'A': 1, 'C': 2, 'D': 5},
    #     'C': {'A': 4, 'B': 2, 'D': 1},
    #     'D': {'B': 5, 'C': 1}
    # }
    #
    # start_node = 'A'
    # distances, predecessors = dijkstra(graph, start_node)
    #
    # # Print the shortest paths and distances
    # for node in graph:
    #     path = []
    #     current_node = node
    #     while current_node is not None:
    #         path.insert(0, current_node)
    #         current_node = predecessors[current_node]
    #
    #     print(f"Shortest path from {start_node} to {node}: {path}, Distance: {distances[node]}")

if __name__ == "__main__":
    main()


    