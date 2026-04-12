from abc import ABC, abstractmethod


class Vehicle(ABC):
    total_vehicles = 0   # class attribute

    def __init__(self, plate_number):
        self.plate_number = plate_number
        Vehicle.total_vehicles += 1

    @abstractmethod
    def get_hourly_rate(self):
        pass

    def __str__(self):
        return f"{self.__class__.__name__} [{self.plate_number}]"

    def __eq__(self, other):
        return self.plate_number == other.plate_number

class Car(Vehicle):
    def get_hourly_rate(self):
        return 20


class Motorcycle(Vehicle):
    def get_hourly_rate(self):
        return 10


class Truck(Vehicle):
    def get_hourly_rate(self):
        return 30