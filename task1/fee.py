import time
import math

class ParkingTicket:
    next_ticket_id = 1   # class attribute

    def __init__(self, vehicle, spot):
        self.ticket_id = ParkingTicket.next_ticket_id
        ParkingTicket.next_ticket_id += 1

        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = time.time()
        self.exit_time = None
        self.fee = 0

    def close_ticket(self):
        self.exit_time = time.time()

    def get_duration_hours(self):
        if self.exit_time is None:
            return 0
        duration = self.exit_time - self.entry_time
        return duration / 3600

    def set_fee(self, fee):
        self.fee = fee

    def __str__(self):
        return f"Ticket {self.ticket_id} | {self.vehicle} | Fee: {self.fee}"
    

class FeeCalculator:

    @staticmethod
    def calculate_hours(entry_time, exit_time):
        duration = exit_time - entry_time
        hours = duration / 3600
        return math.ceil(hours)

    @staticmethod
    def calculate_fee(vehicle, entry_time, exit_time):
        hours = FeeCalculator.calculate_hours(entry_time, exit_time)
        return hours * vehicle.get_hourly_rate()


class PaymentRecord:
    next_payment_id = 1

    def __init__(self, ticket_id, amount, method="Cash"):
        self.payment_id = PaymentRecord.next_payment_id
        PaymentRecord.next_payment_id += 1

        self.ticket_id = ticket_id
        self.amount = amount
        self.method = method
        self.payment_time = time.time()

    def __str__(self):
        return f"Payment {self.payment_id} | Ticket {self.ticket_id} | Amount: {self.amount}"