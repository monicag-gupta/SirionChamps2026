class Vehicle:

    def __init__(self, capacity):
        self.capacity = capacity

    def fare(self):
        return self.capacity * 100


class Bus(Vehicle):

    def fare(self):
        total = super().fare()
        return total + (total * 0.10)


capacity = int(input("Enter bus seating capacity: "))

bus = Bus(capacity)

print("Base Fare:", capacity * 100)
print("Total Bus Fare is:", bus.fare())