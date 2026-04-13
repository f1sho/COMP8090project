import heapq
from mygraph import Graph


def dijkstra_shortest_paths(graph, start_name):
    """Compute shortest distances from start node to every node in the graph."""
    if graph.get_node(start_name) is None:
        raise ValueError(f"Start node '{start_name}' does not exist in the graph.")

    distances = {name: float("inf") for name in graph.get_all_nodes()}
    parent = {}
    distances[start_name] = 0.0

    priority_queue = [(0.0, start_name)]
    visited = set()

    while priority_queue:
        current_distance, current_name = heapq.heappop(priority_queue)
        if current_name in visited:
            continue

        visited.add(current_name)
        current_node = graph.get_node(current_name)
        if current_node is None:
            continue

        for neighbor_node, edge_weight in current_node.get_neighbors().items():
            neighbor_name = neighbor_node.get_name()
            new_distance = current_distance + edge_weight
            if new_distance < distances[neighbor_name]:
                distances[neighbor_name] = new_distance
                parent[neighbor_name] = current_name
                heapq.heappush(priority_queue, (new_distance, neighbor_name))

    return distances, parent


def reconstruct_path(parent_map, target_name, start_name=None):
    """Reconstruct the path from the start node to the target node."""
    path = []
    current_name = target_name

    while current_name is not None:
        path.append(current_name)
        if current_name == start_name:
            break
        current_name = parent_map.get(current_name)

    path.reverse()
    if start_name is not None and path and path[0] != start_name:
        return []

    return path
