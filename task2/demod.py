from mygraph import Graph
from mydijkstra import find_nearest_available_spot


def _build_demo_graph():
    graph = Graph()
    graph.add_edge("Entry_Gate", "Aisle_1", weight=1)
    graph.add_edge("Aisle_1", "Spot_A", weight=2)
    graph.add_edge("Aisle_1", "Spot_B", weight=3)
    graph.add_edge("Aisle_1", "Aisle_2", weight=1)
    graph.add_edge("Aisle_2", "Spot_C", weight=2)
    graph.add_edge("Aisle_2", "Spot_D", weight=4)
    return graph


class DemoSpot:
    """Simple parking spot object for demo usage."""

    def __init__(self, spot_id, is_occupied=False):
        self.spot_id = spot_id
        self.is_occupied = is_occupied

    def __repr__(self):
        return f"DemoSpot({self.spot_id}, occupied={self.is_occupied})"


def main():
    graph = _build_demo_graph()

    parking_spots = [
        DemoSpot("Spot_A", is_occupied=True),
        DemoSpot("Spot_B", is_occupied=False),
        DemoSpot("Spot_C", is_occupied=False),
        DemoSpot("Spot_D", is_occupied=True),
    ]

    result = find_nearest_available_spot(graph, "Entry_Gate", parking_spots)
    if result is None:
        print("No available parking spots found.")
        return

    spot, distance, path = result
    print(f"Nearest available spot: {spot.spot_id}")
    print(f"Distance: {distance}")
    print(f"Path: {' -> '.join(path)}")


if __name__ == "__main__":
    main()
