import time
from mydijkstra import dijkstra_shortest_paths, find_nearest_available_spot, DemoSpot
from mygraph import Graph


def test_basic_functionality():
    """Test 1: Basic functionality - ensure nearest spot is found correctly."""
    print("=" * 60)
    print("TEST 1: Basic Functionality")
    print("=" * 60)
    
    graph = Graph()
    graph.add_edge("Entry_Gate", "Aisle_1", weight=1)
    graph.add_edge("Aisle_1", "Spot_A", weight=2)
    graph.add_edge("Aisle_1", "Spot_B", weight=3)
    graph.add_edge("Aisle_1", "Aisle_2", weight=1)
    graph.add_edge("Aisle_2", "Spot_C", weight=2)
    graph.add_edge("Aisle_2", "Spot_D", weight=4)

    parking_spots = [
        DemoSpot("Spot_A", is_occupied=True),
        DemoSpot("Spot_B", is_occupied=False),
        DemoSpot("Spot_C", is_occupied=False),
        DemoSpot("Spot_D", is_occupied=True),
    ]

    result = find_nearest_available_spot(graph, "Entry_Gate", parking_spots)
    assert result is not None, "Should find available spot"
    spot, distance, path = result
    
    assert spot.spot_id == "Spot_B", f"Expected Spot_B, got {spot.spot_id}"
    assert distance == 4.0, f"Expected distance 4.0, got {distance}"
    print(f"✓ Nearest spot: {spot.spot_id}")
    print(f"✓ Distance: {distance}")
    print(f"✓ Path: {' -> '.join(path)}")
    print()


def test_no_available_spots():
    """Test 2: All spots occupied - should return None."""
    print("=" * 60)
    print("TEST 2: No Available Spots")
    print("=" * 60)
    
    graph = Graph()
    graph.add_edge("Entry", "Spot_A", weight=1)
    graph.add_edge("Entry", "Spot_B", weight=2)

    parking_spots = [
        DemoSpot("Spot_A", is_occupied=True),
        DemoSpot("Spot_B", is_occupied=True),
    ]

    result = find_nearest_available_spot(graph, "Entry", parking_spots)
    assert result is None, "Should return None when no spots available"
    print("✓ Correctly returned None for all occupied spots")
    print()


def test_single_nearest():
    """Test 3: Multiple available spots - nearest one is selected."""
    print("=" * 60)
    print("TEST 3: Single Nearest Among Multiple")
    print("=" * 60)
    
    graph = Graph()
    graph.add_edge("Entry", "A", weight=1)
    graph.add_edge("Entry", "B", weight=1)
    graph.add_edge("A", "Spot_1", weight=1)  # distance: 2
    graph.add_edge("B", "Spot_2", weight=5)  # distance: 6

    parking_spots = [
        DemoSpot("Spot_1", is_occupied=False),
        DemoSpot("Spot_2", is_occupied=False),
    ]

    result = find_nearest_available_spot(graph, "Entry", parking_spots)
    spot, distance, path = result
    
    assert spot.spot_id == "Spot_1", f"Expected Spot_1 (nearest), got {spot.spot_id}"
    assert distance == 2.0, f"Expected distance 2.0, got {distance}"
    print(f"✓ Selected nearest: {spot.spot_id} (distance: {distance})")
    print()


# ==========================================
# TIME COMPLEXITY TESTS
# ==========================================

def build_sparse_graph(num_nodes):
    """Build a sparse graph: E ≈ V (best case for Dijkstra)."""
    graph = Graph()
    for i in range(num_nodes - 1):
        graph.add_edge(f"Node_{i}", f"Node_{i+1}", weight=1)
    return graph


def build_dense_graph(num_nodes):
    """Build a dense graph: E ≈ V² (worst case for Dijkstra)."""
    graph = Graph()
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            graph.add_edge(f"Node_{i}", f"Node_{j}", weight=1, is_directed=True)
    return graph


def test_time_complexity_best_case():
    """Test Best Case: Sparse graph - O(V log V) with heap."""
    print("=" * 60)
    print("TIME COMPLEXITY TEST: BEST CASE (Sparse Graph)")
    print("=" * 60)
    print("Expected: O(V log V) - linear node traversal")
    print()
    
    test_sizes = [100, 500, 1000, 2000]
    
    for size in test_sizes:
        graph = build_sparse_graph(size)
        start_node = "Node_0"
        
        start_time = time.perf_counter()
        distances, parent = dijkstra_shortest_paths(graph, start_node)
        end_time = time.perf_counter()
        
        elapsed = (end_time - start_time) * 1000  # Convert to ms
        print(f"Nodes: {size:4d} | Time: {elapsed:8.4f} ms")


def test_time_complexity_worst_case():
    """Test Worst Case: Dense graph - O((V + E) log V) with heap."""
    print()
    print("=" * 60)
    print("TIME COMPLEXITY TEST: WORST CASE (Dense Graph)")
    print("=" * 60)
    print("Expected: O((V + E) log V) - much slower with many edges")
    print()
    
    test_sizes = [20, 40, 60, 80]  # Smaller sizes for dense graphs
    
    for size in test_sizes:
        graph = build_dense_graph(size)
        start_node = "Node_0"
        num_edges = size * (size - 1) // 2
        
        start_time = time.perf_counter()
        distances, parent = dijkstra_shortest_paths(graph, start_node)
        end_time = time.perf_counter()
        
        elapsed = (end_time - start_time) * 1000  # Convert to ms
        print(f"Nodes: {size:3d} | Edges: {num_edges:6d} | Time: {elapsed:8.4f} ms")


def test_complexity_ratio():
    """Compare ratio between best and worst case."""
    print()
    print("=" * 60)
    print("TIME COMPLEXITY COMPARISON")
    print("=" * 60)
    
    # Test size where both are comparable
    test_size = 50
    
    print(f"\nFor graph with {test_size} nodes:")
    
    # Best case (sparse)
    sparse_graph = build_sparse_graph(test_size)
    start_time = time.perf_counter()
    dijkstra_shortest_paths(sparse_graph, "Node_0")
    sparse_time = (time.perf_counter() - start_time) * 1000
    
    # Worst case (dense)
    dense_graph = build_dense_graph(test_size)
    start_time = time.perf_counter()
    dijkstra_shortest_paths(dense_graph, "Node_0")
    dense_time = (time.perf_counter() - start_time) * 1000
    
    ratio = dense_time / sparse_time if sparse_time > 0 else 0
    
    print(f"  Sparse (E ≈ V):    {sparse_time:8.4f} ms")
    print(f"  Dense (E ≈ V²):    {dense_time:8.4f} ms")
    print(f"  Ratio (Dense/Sparse): {ratio:8.2f}x")
    print()


def main():
    """Run all tests."""
    print("\n")
    print("█" * 60)
    print("  DIJKSTRA ALGORITHM - COMPREHENSIVE TEST SUITE")
    print("█" * 60)
    print()
    
    # Correctness tests
    test_basic_functionality()
    test_no_available_spots()
    test_single_nearest()
    
    # Time complexity tests
    test_time_complexity_best_case()
    test_time_complexity_worst_case()
    test_complexity_ratio()
    
    print("=" * 60)
    print("ALL TESTS COMPLETED!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
