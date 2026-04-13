class Node:
    """
    A class to represent a physical location (Node/Vertex) in the parking lot.
    Each node has a name and a list of neighboring nodes with the distance/weight to each neighbor.
    """
    def __init__(self, name):
        self.name = name
        # Adjacency list implemented as a dictionary.
        # Key: Neighboring Node object | Value: Distance/Weight (int or float)
        self.neighbors = {} 

    # Adds a directed connection from this node to a neighbor node.
    def add_neighbor(self, neighbor_node, weight):

        self.neighbors[neighbor_node] = weight

    # Returns the dictionary of all connected neighbors.
    def get_neighbors(self):

        return self.neighbors
        
    # Returns the name of the node.
    def get_name(self):
        
        return self.name

    # Overrides the default string representation for easier debugging.
    def __str__(self):
        
        return f"Node({self.name})"


class Graph:
    """
    Class to represent the entire parking lot map as a Graph.
    It manages all the nodes and the edges (driving paths) between them.
    """
    def __init__(self):
        # A dictionary to store all nodes in the graph.
        # Key: Node name (string) | Value: Node object
        self.nodes = {}

    def add_node(self, name):
        """
        Creates a new Node and adds it to the graph.
        If the node already exists, it simply returns the existing node.
        """
        if name not in self.nodes:
            new_node = Node(name)
            self.nodes[name] = new_node
            return new_node
        return self.nodes[name]

    def add_edge(self, src_name, dest_name, weight, is_directed=False):
        """
        Creates a driving path (edge) between two nodes.
        
        Parameters:
        - src_name: The starting location name.
        - dest_name: The destination location name.
        - weight: The distance or driving time between them.
        - is_directed: False if cars can drive both ways, True if it's a one-way aisle.
        """
        # Ensure both nodes exist in the graph before connecting them
        if src_name not in self.nodes:
            self.add_node(src_name)
        if dest_name not in self.nodes:
            self.add_node(dest_name)

        src_node = self.nodes[src_name]
        dest_node = self.nodes[dest_name]

        # Add the connection from source to destination
        src_node.add_neighbor(dest_node, weight)

        # If it is a two-way street, add the reverse connection as well
        if not is_directed:
            dest_node.add_neighbor(src_node, weight)

    # Returns a list of all node names in the graph.
    def get_all_nodes(self):
        
        return list(self.nodes.keys())

    # Returns a specific Node object by its name. Returns None if not found.
    def get_node(self, name):
        
        return self.nodes.get(name)


# ==========================================
# test
# ==========================================
if __name__ == "__main__":
    # 1. Initialize the Graph
    parking_lot = Graph()

    # 2. Add edges to build the simple parking lot we discussed
    # (Adding an edge automatically creates the nodes if they don't exist)
    parking_lot.add_edge("Entry_Gate", "Aisle_1", weight=1)
    parking_lot.add_edge("Aisle_1", "Spot_A", weight=1)
    parking_lot.add_edge("Aisle_1", "Spot_B", weight=1)
    parking_lot.add_edge("Aisle_1", "Aisle_2", weight=1)
    parking_lot.add_edge("Aisle_2", "Spot_C", weight=1)
    parking_lot.add_edge("Aisle_2", "Spot_D", weight=1)

    # 3. Print out the connections to verify it works
    print("--- Parking Lot Graph Structure ---")
    for node_name in parking_lot.get_all_nodes():
        node_obj = parking_lot.get_node(node_name)
        neighbors = {}
        if node_obj is not None:
            neighbors = node_obj.get_neighbors()
        
        # Format the output to show connected nodes and their distances
        connections = [f"{neighbor.get_name()} (dist:{weight})" for neighbor, weight in neighbors.items()]
        print(f"{node_name} is connected to: {', '.join(connections)}")