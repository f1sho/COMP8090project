from abc import ABC, abstractmethod


class ParkingSpot(ABC):
    """
    Abstract base class for all parking spot types.
    Each parking spot has:
    - a unique spot ID
    - a distance value
    - an occupancy status
    - a rate per minute
    """

    def __init__(self, spot_id, distance=0, rate_per_minute=0):
        self.spot_id = spot_id
        self.distance = distance
        self.rate_per_minute = rate_per_minute
        self.is_occupied = False

    @abstractmethod
    def can_fit(self, vehicle):
        """
        Return True if the given vehicle can park in this spot.
        Must be implemented by subclasses.
        """
        pass

    def occupy(self):
        """Mark the parking spot as occupied."""
        self.is_occupied = True

    def release(self):
        """Mark the parking spot as available."""
        self.is_occupied = False

    def get_rate_per_minute(self):
        return self.rate_per_minute

    def __lt__(self, other):
        """
        Compare two parking spots by distance.
        Useful for sorting parking spots by shortest distance.
        """
        return self.distance < other.distance

    def __str__(self):
        """
        Return a user-friendly string representation.
        """
        status = "Occupied" if self.is_occupied else "Available"
        return f"{self.__class__.__name__}(ID={self.spot_id}, Status={status}, Distance={self.distance})"


class RegularCarSpot(ParkingSpot):
    def __init__(self, spot_id, distance=0):
        super().__init__(spot_id, distance, rate_per_minute=20/60)

    def can_fit(self, vehicle):
        return vehicle.__class__.__name__ == "Car"


class TruckSpot(ParkingSpot):
    def __init__(self, spot_id, distance=0):
        super().__init__(spot_id, distance, rate_per_minute=35/60)

    def can_fit(self, vehicle):
        return vehicle.__class__.__name__ == "Truck"


class EVChargingSpot(ParkingSpot):
    def __init__(self, spot_id, distance=0):
        super().__init__(spot_id, distance, rate_per_minute=25/60)

    def can_fit(self, vehicle):
        return vehicle.__class__.__name__ == "Car"



