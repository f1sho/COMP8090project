from mygraph import Graph
from mydijkstra import dijkstra_shortest_paths, reconstruct_path
from parking_spot import RegularCarSpot, EVChargingSpot, TruckSpot


class ParkingLot:
    """
    Parking lot management system for the custom layout.

    Layout:
    - Gate
    - Main_Junction
    - 3 aisles
    - 5 parking lanes

    Aisle mapping:
    - Aisle_1 serves Lane_1 and Lane_2
    - Aisle_2 serves Lane_3 and Lane_4
    - Aisle_3 serves Lane_4 and Lane_5

    Distances:
    - Gate <-> Main_Junction = 1
    - Main_Junction <-> Aisle_1 = 1
    - Main_Junction <-> Aisle_2 = 3
    - Main_Junction <-> Aisle_3 = 4

    All roads are two-way.
    """

    def __init__(self):
        self.graph = Graph()
        self.spots = {}

        self._build_spots()
        self._build_graph()

    # =========================================================
    # Build parking spots
    # =========================================================
    def _build_spots(self):
        # Lane 1: EV spots
        for i in range(1, 7):
            spot_id = f"EV{i}"
            self.spots[spot_id] = EVChargingSpot(spot_id)

        # Lane 2: Regular spots
        for i in range(1, 7):
            spot_id = f"R1_{i}"
            self.spots[spot_id] = RegularCarSpot(spot_id)

        # Lane 3: Regular spots
        for i in range(1, 7):
            spot_id = f"R2_{i}"
            self.spots[spot_id] = RegularCarSpot(spot_id)

        # Lane 4: Regular spots
        for i in range(1, 7):
            spot_id = f"R3_{i}"
            self.spots[spot_id] = RegularCarSpot(spot_id)

        # Lane 5: Truck spots
        for i in range(1, 7):
            spot_id = f"T{i}"
            self.spots[spot_id] = TruckSpot(spot_id)

    # =========================================================
    # Build graph map
    # =========================================================
    def _build_graph(self):
        # Core nodes
        self.graph.add_node("Gate")
        self.graph.add_node("Main_Junction")

        aisle_names = ["Aisle_1", "Aisle_2", "Aisle_3"]
        lane_names = ["Lane_1", "Lane_2", "Lane_3", "Lane_4", "Lane_5"]

        for aisle in aisle_names:
            self.graph.add_node(aisle)

        for lane in lane_names:
            self.graph.add_node(lane)

        # Gate to main junction
        self.graph.add_edge("Gate", "Main_Junction", weight=1)

        # Main junction to aisles
        self.graph.add_edge("Main_Junction", "Aisle_1", weight=1)
        self.graph.add_edge("Main_Junction", "Aisle_2", weight=3)
        self.graph.add_edge("Main_Junction", "Aisle_3", weight=4)

        # Aisles to lanes
        # Aisle 1 serves Lane 1 and Lane 2
        self.graph.add_edge("Aisle_1", "Lane_1", weight=1)
        self.graph.add_edge("Aisle_1", "Lane_2", weight=1)

        # Aisle 2 serves Lane 3 and Lane 4
        self.graph.add_edge("Aisle_2", "Lane_3", weight=1)
        self.graph.add_edge("Aisle_2", "Lane_4", weight=1)

        # Aisle 3 serves Lane 4 and Lane 5
        self.graph.add_edge("Aisle_3", "Lane_4", weight=1)
        self.graph.add_edge("Aisle_3", "Lane_5", weight=1)

        # Lane 1 -> EV row
        for i in range(1, 7):
            spot_id = f"EV{i}"
            self.graph.add_node(spot_id)
            self.graph.add_edge("Lane_1", spot_id, weight=i)

        # Lane 2 -> Regular row 1
        for i in range(1, 7):
            spot_id = f"R1_{i}"
            self.graph.add_node(spot_id)
            self.graph.add_edge("Lane_2", spot_id, weight=i)

        # Lane 3 -> Regular row 2
        for i in range(1, 7):
            spot_id = f"R2_{i}"
            self.graph.add_node(spot_id)
            self.graph.add_edge("Lane_3", spot_id, weight=i)

        # Lane 4 -> Regular row 3
        for i in range(1, 7):
            spot_id = f"R3_{i}"
            self.graph.add_node(spot_id)
            self.graph.add_edge("Lane_4", spot_id, weight=i)

        # Lane 5 -> Truck row
        for i in range(1, 7):
            spot_id = f"T{i}"
            self.graph.add_node(spot_id)
            self.graph.add_edge("Lane_5", spot_id, weight=i)

    # =========================================================
    # Display helpers
    # =========================================================
    def display_layout(self):
        """
        Print the parking lot layout.

        E = EVChargingSpot
        R = RegularCarSpot
        T = TruckSpot

        O = available
        X = occupied
        """
        print("\n================ PARKING LOT LAYOUT ================")

        rows = [
            [f"EV{i}" for i in range(1, 7)],
            [f"R1_{i}" for i in range(1, 7)],
            [f"R2_{i}" for i in range(1, 7)],
            [f"R3_{i}" for i in range(1, 7)],
            [f"T{i}" for i in range(1, 7)],
        ]

        for row in rows:
            display_items = []
            for spot_id in row:
                spot = self.spots[spot_id]

                if isinstance(spot, EVChargingSpot):
                    spot_type = "E"
                elif isinstance(spot, TruckSpot):
                    spot_type = "T"
                else:
                    spot_type = "R"

                status = "X" if spot.is_occupied else "O"
                display_items.append(f"{spot_id}[{spot_type},{status}]")

            print("  ".join(display_items))

        print("====================================================\n")


    # =========================================================
    # Spot queries
    # =========================================================
    def get_spot(self, spot_id):
        return self.spots.get(spot_id)

    def get_available_spots_for_vehicle(self, vehicle, requires_ev=False, prefer_regular=False):
        """
        Return a list of available ParkingSpot objects
        that can fit the given vehicle.

        For Car:
        - requires_ev=True   -> only EVChargingSpot
        - prefer_regular=True -> only RegularCarSpot
        - otherwise -> any spot that can fit
        """
        candidates = []

        for spot in self.spots.values():
            if spot.is_occupied:
                continue

            if not spot.can_fit(vehicle):
                continue

            if vehicle.__class__.__name__ == "Car":
                if requires_ev:
                    if not isinstance(spot, EVChargingSpot):
                        continue
                elif prefer_regular:
                    if not isinstance(spot, RegularCarSpot):
                        continue

            candidates.append(spot)

        return candidates

    # =========================================================
    # Dijkstra integration
    # =========================================================
    def find_nearest_available_spot(self, vehicle, requires_ev=False, start_name="Gate"):
        """
        Find the nearest available spot for the given vehicle.

        Returns:
        - (spot_object, distance, path)
        or None if no suitable spot is found
        """
        distances, parent = dijkstra_shortest_paths(self.graph, start_name)

        # -------------------------------------------------
        # Car logic:
        # 1. requires_ev=True  -> only EV spots
        # 2. requires_ev=False -> prefer Regular spots
        #    if no Regular spots available, fallback to EV spots
        # -------------------------------------------------
        if vehicle.__class__.__name__ == "Car":
            if requires_ev:
                candidate_spots = self.get_available_spots_for_vehicle(vehicle, requires_ev=True)
            else:
                candidate_spots = self.get_available_spots_for_vehicle(
                    vehicle,
                    requires_ev=False,
                    prefer_regular=True
                )

                if not candidate_spots:
                    candidate_spots = self.get_available_spots_for_vehicle(
                        vehicle,
                        requires_ev=False,
                        prefer_regular=False
                    )
                    candidate_spots = [
                        spot for spot in candidate_spots
                        if isinstance(spot, EVChargingSpot)
                    ]
        else:
            candidate_spots = self.get_available_spots_for_vehicle(vehicle, requires_ev=False)

        if not candidate_spots:
            return None

        nearest_spot = None
        nearest_distance = float("inf")
        nearest_path = []

        for spot in candidate_spots:
            spot_node_name = spot.spot_id
            distance = distances.get(spot_node_name, float("inf"))

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_spot = spot
                nearest_path = reconstruct_path(parent, spot_node_name, start_name)

        if nearest_spot is None or nearest_distance == float("inf"):
            return None

        nearest_spot.distance = nearest_distance
        return nearest_spot, nearest_distance, nearest_path

    # =========================================================
    # Parking operations
    # =========================================================
    def park_vehicle(self, vehicle, requires_ev=False, start_name="Gate"):
        result = self.find_nearest_available_spot(vehicle, requires_ev, start_name)

        if result is None:
            return None

        spot, distance, path = result
        spot.occupy()
        return spot, distance, path

    def release_spot(self, spot_id):
        spot = self.get_spot(spot_id)
        if spot is None:
            return False

        spot.release()
        return True
