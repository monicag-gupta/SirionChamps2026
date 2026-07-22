# Roman Converter

class RomanConverterCal:

    def int_2_roman(self, num):
        values = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4, 1
        ]

        symbols = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV", "I"
        ]

        roman = ""

        for i in range(len(values)):
            while num >= values[i]:
                roman += symbols[i]
                num -= values[i]

        return roman

    def roman_2_int(self, roman):
        roman_dict = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        total = 0
        prev = 0

        for ch in roman[::-1]:
            value = roman_dict[ch]

            if value < prev:
                total -= value
            else:
                total += value

            prev = value

        return total


obj = RomanConverterCal()

print("Integer to Roman:", obj.int_2_roman(1996))
print("Roman to Integer:", obj.roman_2_int("MCDXCIV"))








# Reversing the string

class ReverseString:

    def reverse_words(self, text):
        words = text.split()
        words.reverse()
        return " ".join(words)


obj = ReverseString()

text = "Hello World"
print("Input :", text)
print("Output:", obj.reverse_words(text))












# inheriting from the vehicle class
class Vehicle:

    def __init__(self, capacity):
        self.capacity = capacity

    def fare(self):
        return self.capacity * 100


class Bus(Vehicle):

    def fare(self):
        total = super().fare()
        maintenance = total * 0.10
        return total + maintenance


bus = Bus(50)

print("Total Bus fare is:", bus.fare())


