import time
import math

# True  -> use simulated parking duration for demonstration
# False -> use real elapsed time
DEMO_MODE = True


class ParkingTicket:
    """
    A class to represent a parking ticket.
    It stores the parked vehicle, allocated parking spot,
    entry/exit time, parking duration in minutes, and final fee.
    """
    next_ticket_id = 1

    def __init__(self, vehicle, spot):
        self.ticket_id = ParkingTicket.next_ticket_id
        ParkingTicket.next_ticket_id += 1

        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = time.time()
        self.exit_time = None
        self.duration_minutes = 0
        self.fee = 0.0

    def close_ticket(self):
        self.exit_time = time.time()

    def set_duration_minutes(self, minutes):
        self.duration_minutes = minutes

    def set_fee(self, fee):
        self.fee = fee

    def __str__(self):
        return (
            f"Ticket {self.ticket_id} | {self.vehicle} | "
            f"Spot: {self.spot.spot_id} | "
            f"Minutes: {self.duration_minutes} | Fee: {self.fee:.2f}"
        )


class FeeCalculator:
    """
    A helper class for fee calculation.
    Charging is based on parking spot type.
    """

    @staticmethod
    def generate_simulated_minutes():
        """
        Return a fixed simulated duration for demonstration.
        This keeps the demo simple and avoids using real waiting time.
        """
        return 45

    @staticmethod
    def calculate_real_minutes(entry_time, exit_time):
        """
        Calculate real parking duration in minutes.
        At least 1 minute will be charged.
        """
        duration_seconds = exit_time - entry_time
        return max(1, math.ceil(duration_seconds / 60))

    @staticmethod
    def calculate_fee_by_minutes(spot, minutes):
        """
        Calculate fee based on the parking spot rate per minute.
        """
        return minutes * spot.get_rate_per_minute()

    @staticmethod
    def checkout(ticket):
        """
        Complete checkout:
        - record exit time
        - determine duration (demo or real mode)
        - calculate fee based on spot type
        - store results in the ticket

        Returns:
        - duration_minutes
        - fee
        """
        ticket.close_ticket()

        if DEMO_MODE:
            duration_minutes = FeeCalculator.generate_simulated_minutes()
        else:
            duration_minutes = FeeCalculator.calculate_real_minutes(
                ticket.entry_time, ticket.exit_time
            )

        fee = FeeCalculator.calculate_fee_by_minutes(ticket.spot, duration_minutes)

        ticket.set_duration_minutes(duration_minutes)
        ticket.set_fee(fee)

        return duration_minutes, fee