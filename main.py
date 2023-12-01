import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from Dijkstra import dijkstra, get_shortest_path
from AStar import astar
import time
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
            if node2 not in adjacency_list:
                adjacency_list[node2] = []
            adjacency_list[node1].append((node2, weight))
            adjacency_list[node2].append((node1, weight))

    return edges, adjacency_list


def create_graph(nodes, edges):
    G = nx.Graph()

    # Add nodes with positions
    for node_id, pos in nodes.items():
        G.add_node(node_id, pos=pos)

    # Add edges with attributes
    G.add_edges_from(edges)

    return G

def draw_graph(G, path_edges=None, path=None):
    node_positions = nx.get_node_attributes(G, 'pos')
    fig, ax = plt.subplots(figsize=(10, 7))  # Adjust the size as needed

    # Draws the graph
    nx.draw_networkx(G, node_positions, with_labels=False, node_size=1, node_color='skyblue', font_size=6, font_color='black', edge_color='gray', ax=ax)

    # Highlights the shortest path
    if path_edges:
        nx.draw_networkx_edges(G, edgelist=path_edges, edge_color='black', width=2, pos=node_positions)  # Include pos=node_positions
    if path:
        nx.draw_networkx_nodes(G, nodelist=path, node_size=1, node_color='red', pos=node_positions) # use another path list to highlight key nodes on roadtrip

    plt.show()


def color_path(G, path):
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    return path_edges


def main():
    print("Welcome to Optim")
    nodes_file = input("Enter the node file.\n")
    edges_file = input("Enter the edge file.\n")

    # Read nodes and edges from files
    nodes = read_nodes(nodes_file)
    edges, adjacencyList = read_edges(edges_file)

    road_trip = input("Enter all node values that you want to visit, in the order you want to visit them. Ex: \"24 65 75 90\"\n").split()
    algorithm = int(input("1. Dijkstra's\n2. A*\n"))

    # TODO CALL THE ALGORITHMS MULTIPLE TIMES
    if algorithm == 1:
        start = time.time()
        distances, predecessors = dijkstra(adjacencyList, int(road_trip[0]), int(road_trip[-1]))
        end = time.time()
        path = get_shortest_path(predecessors, int(road_trip[0]), int(road_trip[-1]))
        print(end - start)

    elif algorithm == 2:
        start = time.time()
        path = astar(adjacencyList, int(road_trip[0]), int(road_trip[-1]), nodes)
        end = time.time()
        print(end - start)

    # create Graph
    graph = create_graph(nodes, edges)

    path_edges = color_path(graph, path)

    # Draw the graph
    draw_graph(graph, path_edges, path)


if __name__ == "__main__":
    main()


    