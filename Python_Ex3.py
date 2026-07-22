class Vehicle:
    def __init__(self, seating_capacity):
        self.seating_capacity = seating_capacity

    def fare(self):
        return self.seating_capacity * 100


class Bus(Vehicle):
    def fare(self):
        total = super().fare()
        return total + (0.1 * total)


bus = Bus(50)
print("Total Bus fare is:", bus.fare())
