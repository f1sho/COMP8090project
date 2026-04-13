from abc import ABC


class Vehicle(ABC):
    total_vehicles = 0

    def __init__(self, plate_number):
        self.plate_number = plate_number
        Vehicle.total_vehicles += 1

    def __str__(self):
        return f"{self.__class__.__name__} [{self.plate_number}]"

    def __eq__(self, other):
        return isinstance(other, Vehicle) and self.plate_number == other.plate_number


class Car(Vehicle):
    pass


class Truck(Vehicle):
    pass