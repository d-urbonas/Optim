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
            edges.append((node1, node2, {'distance': weight}))
            if node1 not in adjacency_list:
                adjacency_list[node1] = []
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

def draw_graph(G):
    node_positions = nx.get_node_attributes(G, 'pos')
    fig, ax = plt.subplots(figsize=(20, 15))  # Adjust the size as needed
    nx.draw_networkx(G, node_positions, with_labels=False, node_size=1, node_color='skyblue', font_size=1, font_color='black', edge_color='gray', ax=ax)
    plt.show()


def main():
    # File paths
    nodes_file = './input/all_edges.txt'
    edges_file = './input/edges.txt'

    # Read nodes and edges from files
    nodes = read_nodes(nodes_file)
    edges, adjacencyList = read_edges(edges_file)

    # Create graph
    graph = create_graph(nodes, edges)

    # Draw the graph
    draw_graph(graph)
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


    