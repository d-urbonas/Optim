import networkx as nx
import matplotlib as plt
from Dijkstra import dijkstra
plt.use('TkAgg')  # Use the TkAgg backend


def read_nodes(file_path, max_lines=200):
    nodes = {}
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line_num > max_lines:
                break

            node_id, longitude, latitude = map(float, line.strip().split())
            nodes[node_id] = {'longitude': longitude, 'latitude': latitude}

    return nodes

def read_edges(file_path, max_lines=100):
    edges = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line_num > max_lines:
                break

            node1, node2, distance, duration = map(float, line.strip().split())
            edges.append((node1, node2, {'distance': distance, 'duration': duration}))

    return edges


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
    #nx.draw_networkx(G, node_positions, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='gray')
    nx.draw_networkx(G)
    labels = nx.get_edge_attributes(G, 'distance')
    nx.draw_networkx_edge_labels(G, node_positions, edge_labels=labels)


def main():
    # File paths
    nodes_file = 'master_nodes.txt'
    edges_file = 'master_edges.txt'

    # Read nodes and edges from files
    nodes = read_nodes(nodes_file)
    edges = read_edges(edges_file)

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


    