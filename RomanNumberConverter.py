class RomanConverter:
    def int_to_roman(self, num):
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

        roman = ""

        for i in range(len(val)):
            while num >= val[i]:
                roman += syms[i]
                num -= val[i]

        return roman

    def roman_to_int(self, s):
        roman = {
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

        for ch in reversed(s):
            value = roman[ch]
            if value < prev:
                total -= value
            else:
                total += value
            prev = value

        return total


converter = RomanConverter()

number = int(input("Enter an integer (1-3999): "))
roman_numeral = converter.int_to_roman(number)
print("Roman numeral:", roman_numeral)

roman_input = input("Enter a Roman numeral: ").upper()
integer_value = converter.roman_to_int(roman_input)
print("Integer value:", integer_value)
