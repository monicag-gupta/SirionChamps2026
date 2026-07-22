# Parent class
class Vehicle:

    def __init__(self, seating_capacity):
        self.seating_capacity = seating_capacity

    def fare(self):
        return self.seating_capacity * 100


# Child class
class Bus(Vehicle):

    def __init__(self):
        super().__init__(50)   # Bus seating capacity = 50

    # Override fare() method
    def fare(self):
        total_fare = super().fare()
        maintenance = total_fare * 0.10
        return total_fare + maintenance


# Driver Code
bus = Bus()
print("Total Bus fare is:", bus.fare())