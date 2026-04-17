from parking_lot import ParkingLot
from vehicle import Car


def main():
    lot = ParkingLot()

    # Manually occupy all regular spots to test edge case where only EV spots are available
    regular_spots = [
        "R1_1", "R1_2", "R1_3", "R1_4", "R1_5", "R1_6",
        "R2_1", "R2_2", "R2_3", "R2_4", "R2_5", "R2_6",
        "R3_1", "R3_2", "R3_3", "R3_4", "R3_5", "R3_6",
    ]

    for spot_id in regular_spots:
        lot.manually_occupy_spot(spot_id)

    print("=== Parking lot after occupying all regular spots ===")
    lot.display_layout()

    # Now try to park a car that does not require EV charging. It should be allocated an EV spot since all regular spots are occupied.
    car = Car("ABC123")

    result = lot.park_vehicle(car, requires_ev=False)

    print("\n=== Parking result ===")
    if result is None:
        print("No available spot found.")
    else:
        spot, distance, path = result
        print(f"Allocated spot: {spot.spot_id}")
        print(f"Distance: {distance}")
        print(f"Path: {' -> '.join(path)}")

    print("\n=== Parking lot after parking ===")
    lot.display_layout()


if __name__ == "__main__":
    main()