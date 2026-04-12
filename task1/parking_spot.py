from abc import ABC, abstractmethod


class ParkingSpot(ABC):
    def __init__(self, spot_id, distance):
        self.spot_id = spot_id
        self.distance = distance
        self.is_occupied = False

    @abstractmethod
    def can_fit(self, vehicle):
        pass

    def occupy(self):
        self.is_occupied = True

    def release(self):
        self.is_occupied = False

    def __lt__(self, other):
        return self.distance < other.distance

    def __str__(self):
        return f"Spot {self.spot_id} (Occupied: {self.is_occupied})"


class CompactSpot(ParkingSpot):
    def can_fit(self, vehicle):
        return vehicle.__class__.__name__ in ["Car", "Motorcycle"]


class LargeSpot(ParkingSpot):
    def can_fit(self, vehicle):
        return True


class MotorcycleSpot(ParkingSpot):
    def can_fit(self, vehicle):
        return vehicle.__class__.__name__ == "Motorcycle"