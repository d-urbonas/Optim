import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from Dijkstra import dijkstra, reconstruct_path
from AStar import astar
import time
import csv
from matplotlib.animation import FuncAnimation

matplotlib.use('TkAgg')  # Use the TkAgg backend. needed for networkx to work/integrate properly with matplotlib


# reads all the nodes from input file and adds them to a dictionary and where the node_id is the key and the position is the value as a tuple
def read_nodes(file_path):
    nodes = {}
    with open(file_path, 'r') as file:
        for line in file:
            node_id, longitude, latitude = map(float, line.strip().split())
            nodes[node_id] = (longitude, latitude)

    return nodes


# reads edges from file and adds them to edges list while also creating the adj list
def read_edges(file_path, max_lines=180000):
    adjacency_list = {}
    edges = []
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if line_num > max_lines:
                break
            edgeID, node1, node2, weight = map(float, line.strip().split())
            edges.append((node1, node2, {'distance': weight}))

            if node1 not in adjacency_list:  # initialize adj list if it doesn't already exist
                adjacency_list[node1] = []
            if node2 not in adjacency_list:
                adjacency_list[node2] = []
            adjacency_list[node1].append((node2, weight))  # append both ways for undirected graph
            adjacency_list[node2].append((node1, weight))

    return edges, adjacency_list


def create_graph(nodes, edges):
    G = nx.Graph()  # creates the networkx graph object

    # add each node to the graph along with the additional argument of its location to make the graph a valid map
    for node_id, pos in nodes.items():
        G.add_node(node_id, pos=pos)

    # Add edges to graph all at once
    G.add_edges_from(edges)

    return G

def draw_graph(G, time, algorithm, notes_file, path_edges=None, path=None):
    node_positions = nx.get_node_attributes(G, 'pos')
    fig, ax = plt.subplots(figsize=(10, 7))  # set custom window size so not tiny by default
    ax.axis("off") # Turns off the graph axes

    # write time
    if algorithm == 1:
        ax.text(5000, -2000, f"Dijkstra's Algorithm Took {time} Seconds.")
    elif algorithm == 2:
        ax.text(5000, -2000, f"AStar Algorithm Took {time} Seconds.")

    # write notes to screen
    
    with open(notes_file, mode='r') as cur_file:
        # csv_reader is the object for iterating through the csv file
        csv_reader = csv.reader(cur_file, delimiter=',')
        cur_y = -1200 #default y vlaue for text

        # create this dictionary to store notes
        notes_dict = {}

        for row in csv_reader:
            node = row[0]
            note = row[1]

            # adds notes to  dictionary
            notes_dict[node] = note

    # set ensures that a note is only printed once, even if the node is visited multiple times
    notes_keys = set()
    for key in notes_dict.keys():
        notes_keys.add(int(key))

    visited = set()
    # printing notes on screen
    # text(x value, y value, text)
    ax.text(-2300, cur_y - 400, "----------------------")
    ax.text(-2000, cur_y - 800, "Trip Notes")

    # iterate through path and add a note for each hit
    for node_v in path:
        # checks if each node has an associated note
        if int(node_v) in notes_keys:
            # ensures node hasn't been visited
            if int(node_v) not in visited:
                visited.add(int(node_v))
                # prints a note
                ax.text(-3000, cur_y, f'{int(node_v):{8}} | {notes_dict[str(int(node_v))]} ')
                cur_y += 400

    # Draws the graph
    nx.draw_networkx(G, node_positions, with_labels=False, node_size=1, node_color='skyblue', font_size=6,
                     font_color='black', edge_color='gray', ax=ax)

    nodesPerFrame = len(path) // 10  # used to make animation always take the number of frames as defined by the denominator (could require additional frame)

    animation = FuncAnimation(fig, animate_path(G, path_edges, path, node_positions, nodesPerFrame),
                              frames=12, interval=10, repeat=False)  # citing mat plot lib documentation

    plt.show()  # displays graph using matplotlib


def animate_path(G, path_edges, path, node_positions, nodesPerFrame):  # citing matplotlib animation documentation
    def update(frame):
        if frame > 0:
            # path_edges[:(frame * nodesPerFrame)]  this allows all animations to finish in 10/11 frames as nodesPerFrame
            # is dependent on the len of the path and so this always scales proportionally.

            if path_edges:  # color edges in path black
                nx.draw_networkx_edges(G, edgelist=path_edges[:(frame * nodesPerFrame)], edge_color='black', width=2,
                                       pos=node_positions)
            if path:  # color nodes in path orange
                nx.draw_networkx_nodes(G, nodelist=path[:(frame * nodesPerFrame)], node_size=1, node_color='#ff6600',
                                       # dark orange, UF colors yessirski
                                       pos=node_positions)  # use another path list to highlight key nodes on roadtrip

    return update  # returns the result of update which is the argument needed for FuncAnimation function


def edges_to_color(path):  # organizes edges to be colored in way such that they can be pased into networkx function as edge list
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    return path_edges


def main():
    print("Welcome to Optim")

    # get nodes and edges, also create the csv file seeded based on the edges file name
    nodes_file = "./input/" + input("Enter the node file.\n")
    edges_file = "./input/" + input("Enter the edge file.\n")
    notes_file = "./notes/" + edges_file[8:-4] + ".csv"
    # create the csv file if its initially empty
    file = open(notes_file, 'a')
    file.close()
    option = 0
    while option != 3:
        option = int(input("1. Calculate a Trip\n2. Add a note\n3. Exit\n"))
        # note functionality
        if option == 2:
            temp = int(input("Input Node:\n"))
            message = input("Input Note:\n")
            
            # Write node note to notes file

            # csv_writer is object to write (append) new notes to the csv file, so that notes can be saved over time
            with open(notes_file, mode='a') as cur_file:
                csv_writer = csv.writer(cur_file, delimiter=',', lineterminator='')
                # represents a new row to add
                new_row = []

                # add node and note
                new_row.append(temp)
                new_row.append(message + '\n')

                # adds new node, note pair to csv file
                csv_writer.writerow(new_row)
                
        # pathfinding functionality
        elif option == 1:
            # Read nodes and edges from files
            nodes = read_nodes(nodes_file)
            edges, adjacencyList = read_edges(edges_file)

            road_trip = input(
                "Enter all node values that you want to visit, in the order you want to visit them. Ex: \"24 65 75 90\"\n").split()
            algorithm = int(input("1. Dijkstra's\n2. A*\n"))

            path = []  # will hold path returned from search algs
            start = time.time()

            # calculates the path between each inputted node and adds it to the final path arrary
            for i in range(len(road_trip) - 1):
                node1 = road_trip[i]
                node2 = road_trip[i + 1]
                if algorithm == 1:
                    distances, predecessors = dijkstra(adjacencyList, int(node1), int(node2))
                    path.extend(reconstruct_path(predecessors, int(node2)))
                elif algorithm == 2:
                    start = time.time()
                    path.extend(astar(adjacencyList, int(node1), int(node2), nodes))

            end = time.time()
            difference = end - start  # calculate time used

            # create Graph
            graph = create_graph(nodes, edges)

            path_edges = edges_to_color(path)

            # Draw the graph
            draw_graph(graph, difference, algorithm, notes_file, path_edges, path)


if __name__ == "__main__":
    main()
