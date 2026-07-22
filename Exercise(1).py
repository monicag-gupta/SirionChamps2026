class RomanConverter:

    # Integer to Roman
    def int_to_roman(self, num):
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

    # Roman to Integer
    def roman_to_int(self, roman):
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

        for char in reversed(roman):
            value = roman_dict[char]

            if value < prev:
                total -= value
            else:
                total += value

            prev = value

        return total


obj = RomanConverter()

# number = 1994

number=int(input("Enter the number"))
roman = obj.int_to_roman(number)

print("Integer to Roman:", roman)
print("Roman to Integer:", obj.roman_to_int(roman))
