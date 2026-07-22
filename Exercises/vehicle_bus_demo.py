class Vehicle:
    def __init__(self, seating_capacity):
        self.seating_capacity = seating_capacity

    def fare(self):
        return self.seating_capacity * 100


class Bus(Vehicle):
    def fare(self):
        base_fare = super().fare()
        maintenance_charge = 0.10 * base_fare
        return base_fare + maintenance_charge


bus = Bus(50)
print("Total Bus fare is:", bus.fare())
