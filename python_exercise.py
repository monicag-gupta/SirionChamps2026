#Part - 1
class RomanConverter:

    def int_to_roman(self, num):
        values = [
            (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
            (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
            (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
        ]

        roman = ""

        for value, symbol in values:
            while num >= value:
                roman += symbol
                num -= value

        return roman

    def roman_to_int(self, roman):
        values = {
            "I": 1, "V": 5, "X": 10, "L": 50,
            "C": 100, "D": 500, "M": 1000
        }

        total = 0

        for i in range(len(roman)):
            if i + 1 < len(roman) and values[roman[i]] < values[roman[i + 1]]:
                total -= values[roman[i]]
            else:
                total += values[roman[i]]

        return total


converter = RomanConverter()

print(converter.int_to_roman(1994))
print(converter.roman_to_int("MCMXCIV"))



print("\n----------------------\n")

# Part - 2
class StringReverse:

    def reverse_words(self, string):
        words = string.split()
        words.reverse()
        return " ".join(words)


obj = StringReverse()

input_string = "hello world"

print(obj.reverse_words(input_string))



print("\n----------------------\n")

#Part - 3
class Vehicle:

    def __init__(self, seating_capacity):
        self.seating_capacity = seating_capacity

    def fare(self):
        return self.seating_capacity * 100


class Bus(Vehicle):

    def fare(self):
        total_fare = super().fare()
        maintenance_charge = total_fare * 0.10

        final_amount = total_fare + maintenance_charge

        return final_amount


bus = Bus(50)

print("Total Bus fare is:", bus.fare())
