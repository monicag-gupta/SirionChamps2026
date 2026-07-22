class Vehicle:
    def __init__(self, seating_capacity):
        self.seating_capacity = seating_capacity

    def fare(self):
        return self.seating_capacity * 100


class Bus(Vehicle):
    def __init__(self, seating_capacity):
        super().__init__(seating_capacity)

    def fare(self):
        total_fare = super().fare()
        return total_fare + (0.10 * total_fare)


capacity = int(input("Enter bus seating capacity: "))
bus = Bus(capacity)
print("Total Bus fare is:", bus.fare())
