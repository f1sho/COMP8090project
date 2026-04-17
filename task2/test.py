from mygraph import Graph
from mydijkstra import dijkstra_shortest_paths, reconstruct_path


def build_test_graph():
    graph = Graph()

    # Build the same parking lot example
    graph.add_edge("Entry_Gate", "Aisle_1", 1)
    graph.add_edge("Aisle_1", "Spot_A", 1)
    graph.add_edge("Aisle_1", "Spot_B", 1)
    graph.add_edge("Aisle_1", "Aisle_2", 1)
    graph.add_edge("Aisle_2", "Spot_C", 1)
    graph.add_edge("Aisle_2", "Spot_D", 1)

    return graph


def test_dijkstra():
    graph = build_test_graph()

    distances, parent = dijkstra_shortest_paths(graph, "Entry_Gate")

    print("=== Shortest Distances from Entry_Gate ===")
    for node_name, distance in distances.items():
        print(f"{node_name}: {distance}")

    print("\n=== Parent Map ===")
    for node_name, previous_node in parent.items():
        print(f"{node_name} <- {previous_node}")

    print("\n=== Reconstructed Paths ===")
    for target in graph.get_all_nodes():
        path = reconstruct_path(parent, target, "Entry_Gate")
        print(f"Path to {target}: {' -> '.join(path) if path else 'No path'}")

    # Simple checks
    assert distances["Entry_Gate"] == 0.0
    assert distances["Aisle_1"] == 1.0
    assert distances["Spot_A"] == 2.0
    assert distances["Spot_B"] == 2.0
    assert distances["Aisle_2"] == 2.0
    assert distances["Spot_C"] == 3.0
    assert distances["Spot_D"] == 3.0

    assert reconstruct_path(parent, "Spot_C", "Entry_Gate") == [
        "Entry_Gate", "Aisle_1", "Aisle_2", "Spot_C"
    ]

    print("\nAll tests passed.")


if __name__ == "__main__":
    test_dijkstra()