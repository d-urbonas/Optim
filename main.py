import networkx as nx
import matplotlib.pyplot as plt

def read_nodes(file_path):
    nodes = {}
    with open(file_path, 'r') as file:
        for line in file:
            node_id, longitude, latitude = map(float, line.strip().split())
            nodes[node_id] = {'longitude': longitude, 'latitude': latitude}
    return nodes

def read_edges(file_path):
    edges = []
    with open(file_path, 'r') as file:
        for line in file:
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
    # nx.draw_networkx(G, node_positions, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black', edge_color='gray')
    nx.draw_networkx(G)
    labels = nx.get_edge_attributes(G, 'distance')
    nx.draw_networkx_edge_labels(G, node_positions, edge_labels=labels)
    plt.show()

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

if __name__ == "__main__":
    main()


    