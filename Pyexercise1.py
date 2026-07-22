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
        roman_values = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000
        }

        total = 0

        for i in range(len(roman)):
            if i < len(roman) - 1 and roman_values[roman[i]] < roman_values[roman[i + 1]]:
                total -= roman_values[roman[i]]
            else:
                total += roman_values[roman[i]]

        return total


# Driver Code
obj = RomanConverter()

# Integer to Roman
num = int(input("Enter an integer: "))
print("Roman Numeral:", obj.int_to_roman(num))

# Roman to Integer
roman = input("Enter a Roman Numeral: ")
print("Integer:", obj.roman_to_int(roman))