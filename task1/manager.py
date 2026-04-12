class Manager:

    def __init__(self):
        self.total_revenue = 0
        self.total_vehicles = 0

    def record_payment(self, amount):
        self.total_revenue += amount
        self.total_vehicles += 1

    def get_average_fee(self):
        if self.total_vehicles == 0:
            return 0
        return self.total_revenue / self.total_vehicles

    def __str__(self):
        return f"Revenue: {self.total_revenue}, Vehicles: {self.total_vehicles}"