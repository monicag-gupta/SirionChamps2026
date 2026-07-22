class Vehicle:

    def __init__(self, name, seating_capacity):
        self.name = name
        self.seating_capacity = seating_capacity

    def fare(self):
        # Default fare: Capacity * 100
        return self.seating_capacity * 100


class Bus(Vehicle):

    def fare(self):
        # Step 1: Get the base fare from the parent class
        base_fare = super().fare()

        # Step 2: Add 10% extra as maintenance charge
        maintenance_charge = base_fare * 0.10
        total_fare = base_fare + maintenance_charge

        return total_fare


# --- Interactive Main Program ---
print("--- Vehicle Fare Calculator ---")
vehicle_type = input(
    "What type of vehicle would you like to calculate fare for? (enter 'bus' or 'vehicle'): "
).lower()

if vehicle_type == "bus":
    # Default seating capacity for a bus is 50
    capacity_input = input("Enter seating capacity (press Enter to use default 50): ")

    if capacity_input.strip() == "":
        bus_capacity = 50
    else:
        bus_capacity = int(capacity_input)

    # Create Bus object
    school_bus = Bus("School Bus", bus_capacity)
    print(f"Total Bus fare is: {school_bus.fare()}")

else:
    vehicle_name = input("Enter vehicle name: ")
    capacity = int(input("Enter seating capacity: "))

    # Create generic Vehicle object
    general_vehicle = Vehicle(vehicle_name, capacity)
    print(f"Total {general_vehicle.name} fare is: {general_vehicle.fare()}")