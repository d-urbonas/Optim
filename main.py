import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from Dijkstra import dijkstra, get_shortest_path
from AStar import astar
import time
import csv
from matplotlib.animation import FuncAnimation

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
    fig, ax = plt.subplots(figsize=(10, 7))  # set custom window size so not tiny by default
    
    # write notes to screen
    notes_file = "node_notes.csv"
    with open(notes_file, mode='r') as cur_file:
        csv_reader = csv.reader(cur_file, delimiter=',')
        line_count = 0
        cur_y = 40

        for row in csv_reader:
            node = row[0]
            note = row[1]

            ax.text(100, cur_y, f'{node:{8}} | {note} ')
            cur_y += 400


    # Draws the graph
    nx.draw_networkx(G, node_positions, with_labels=False, node_size=1, node_color='skyblue', font_size=6, font_color='black', edge_color='gray', ax=ax)

    nodesPerFrame = len(path) // 10  # used to make animation always take the number of frames as defined by the denominator (could require additional frame)

    animation = FuncAnimation(fig, animate_path(G, path_edges, path, node_positions, nodesPerFrame),  # citing mat plot lib documentation
                         12, interval=10, repeat=False)

    plt.show()

def animate_path(G, path_edges, path, node_positions, nodesPerFrame):  # citing matplotlib animation documentation
    def update(frame):
        if frame > 0:
            # path_edges[:(frame * nodesPerFrame)]  this allows all animations to finish in 10/11 frames as nodesPerFrame
            # is dependent on the len of the path and so this always scales proportionally.
            if path_edges:  # color edges in path blacl
                nx.draw_networkx_edges(G, edgelist=path_edges[:(frame*nodesPerFrame)], edge_color='black', width=2,
                                       pos=node_positions)
            if path:  # color nodes in path orange
                nx.draw_networkx_nodes(G, nodelist=path[:(frame*nodesPerFrame)], node_size=1, node_color='#ff6600', # dark orange, UF colors yessirski
                                       pos=node_positions)  # use another path list to highlight key nodes on roadtrip

    return update  # returns the result of update which is the argument needed for FuncAnimation function

def color_path(G, path):  # organizes edges to be colored in way such that they can be pased into networkx function as edge list
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    return path_edges


def main():
    print("Welcome to Optim")
    nodes_file = input("Enter the node file.\n")
    edges_file = input("Enter the edge file.\n")
    notes_file = "node_notes.csv"

    option = 0
    while option != 3:
        option = int(input("1. Calculate a Trip\n2. Add a note\n3. Exit\n"))

        if option == 2:
            temp = int(input("Input Node:\n"))
            message = input("Input Note:\n")
            # Write node note to notes file

            with open(notes_file, mode='a') as cur_file:
                csv_writer = csv.writer(cur_file, delimiter=',')
                new_row = []
                new_row.append(temp)
                new_row.append(message)

                csv_writer.writerow(new_row)

        elif option == 1:
            # Read nodes and edges from files
            nodes = read_nodes(nodes_file)
            edges, adjacencyList = read_edges(edges_file)

            road_trip = input("Enter all node values that you want to visit, in the order you want to visit them. Ex: \"24 65 75 90\"\n").split()
            algorithm = int(input("1. Dijkstra's\n2. A*\n"))

            path = []
            for i in range(len(road_trip) - 1):
                node1 = road_trip[i]
                node2 = road_trip[i + 1]
                if algorithm == 1:
                    start = time.time()
                    distances, predecessors = dijkstra(adjacencyList, int(node1), int(node2))
                    end = time.time()
                    path.extend(get_shortest_path(predecessors, int(node1), int(node2)))
                    #print(end - start)
                elif algorithm == 2:
                    start = time.time()
                    path.extend(astar(adjacencyList, int(node1), int(node1), nodes))
                    end = time.time()
                    #print(end - start)

            # create Graph
            graph = create_graph(nodes, edges)

            path_edges = color_path(graph, path)

            # Draw the graph
            draw_graph(graph, path_edges, path)


if __name__ == "__main__":
    main()


    
