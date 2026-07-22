class Vehicle:

    def __init__(self, capacity):
        self.capacity = capacity

    def fare(self):
        return self.capacity * 100


class Bus(Vehicle):

    def fare(self):
        amount = super().fare()
        return amount + amount * 0.10


bus = Bus(50)
print("Total Bus fare is:", bus.fare())
