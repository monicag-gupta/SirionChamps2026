class RomanConverter:

    def int_to_roman(self, num):
        values = [1000, 900, 500, 400, 100, 90, 50, 40,
                  10, 9, 5, 4, 1]
        symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL",
                   "X", "IX", "V", "IV", "I"]

        roman = ""
        i = 0

        while num > 0:
            while num >= values[i]:
                roman += symbols[i]
                num -= values[i]
            i += 1

        return roman

    def roman_to_int(self, roman):
        roman_dict = {
            "I": 1, "V": 5, "X": 10,
            "L": 50, "C": 100,
            "D": 500, "M": 1000
        }

        total = 0
        prev = 0

        for char in reversed(roman.upper()):
            value = roman_dict[char]
            if value < prev:
                total -= value
            else:
                total += value
            prev = value

        return total


converter = RomanConverter()

print("1. Integer to Roman")
print("2. Roman to Integer")
choice = int(input("Enter your choice: "))

if choice == 1:
    number = int(input("Enter an integer: "))
    print("Roman Numeral:", converter.int_to_roman(number))

elif choice == 2:
    roman = input("Enter a Roman numeral: ")
    print("Integer:", converter.roman_to_int(roman))

else:
    print("Invalid choice!")