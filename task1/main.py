from parking_lot import ParkingLot
from vehicle import Car, Truck
from fee import ParkingTicket, FeeCalculator
from ui import ParkingLotUI


def create_vehicle():
    """
    Create a vehicle object from user input.

    Returns:
    - (vehicle, requires_ev)
    or
    - (None, False) if invalid
    """
    vehicle_type = input("Enter vehicle type (car / truck): ").strip().lower()
    plate_number = input("Enter plate number: ").strip().upper()

    if vehicle_type == "car":
        ev_input = input("Need EV charging spot? (y/n): ").strip().lower()
        requires_ev = (ev_input == "y")
        return Car(plate_number), requires_ev

    elif vehicle_type == "truck":
        return Truck(plate_number), False

    else:
        print("Invalid vehicle type.")
        return None, False
    

def pause():
    input("\nPress Enter to continue...")


def main():
    parking_lot = ParkingLot()

    # plate_number -> ParkingTicket
    active_tickets = {}

    # For graphical display of the most recent route
    last_path = None
    last_assigned_spot = None

    while True:
        print("\n------------ SMART PARKING SYSTEM ------------")
        print("1. Display parking lot status")
        print("2. Park a vehicle")
        print("3. Checkout and calculate fee")
        print("4. Show graphical UI")
        print("5. Exit")
        print("-----------------------------------------------")

        choice = input("Enter your choice: ").strip()

        # -------------------------------------------------
        # 1. Display layout
        # -------------------------------------------------
        if choice == "1":
            parking_lot.display_layout()
            pause()

        # -------------------------------------------------
        # 2. Park a vehicle
        # -------------------------------------------------
        elif choice == "2":
            vehicle, requires_ev = create_vehicle()

            if vehicle is None:
                continue

            if vehicle.plate_number in active_tickets:
                print("================================================")
                print("This vehicle is already parked in the system.")
                pause()
                continue

            result = parking_lot.park_vehicle(vehicle, requires_ev=requires_ev)

            if result is None:
                print("================================================")
                print("No suitable parking spot found.")

            else:
                spot, distance, path = result

                ticket = ParkingTicket(vehicle, spot)
                active_tickets[vehicle.plate_number] = ticket

                last_path = path
                last_assigned_spot = spot.spot_id

                print("\n================================================")
                print("Vehicle parked successfully.")
                print("Allocated spot:", spot.spot_id)
                print("Distance:", distance)
                print("Path:", " -> ".join(path))
                print("Ticket created for plate:", vehicle.plate_number)

            pause()

        # -------------------------------------------------
        # 3. Checkout and calculate fee
        # -------------------------------------------------
        elif choice == "3":
            plate_number = input("Enter plate number for checkout: ").strip().upper()
            ticket = active_tickets.get(plate_number)

            if ticket is None:
                print("No active ticket found for this vehicle.")
                pause()
                continue

            duration_minutes, fee = FeeCalculator.checkout(ticket)

            print("\n============== CHECKOUT RESULT ==============")
            print("Vehicle:", ticket.vehicle)
            print("Spot:", ticket.spot.spot_id)
            print("Duration:", duration_minutes, "minute(s)")
            print("Fee:", f"{fee:.2f}")
            print("=============================================\n")

            parking_lot.release_spot(ticket.spot.spot_id)
            del active_tickets[plate_number]

            # Clear recent highlighted path after checkout
            last_path = None
            last_assigned_spot = None

            pause()

        # -------------------------------------------------
        # 4. Show graphical UI
        # -------------------------------------------------
        elif choice == "4":
            ui = ParkingLotUI(parking_lot)
            ui.run(path=last_path, assigned_spot_id=last_assigned_spot)

        # -------------------------------------------------
        # 5. Exit
        # -------------------------------------------------
        elif choice == "5":
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()