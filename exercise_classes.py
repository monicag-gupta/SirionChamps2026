class RomanNumeralConverter:
    values = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    roman_map = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000,
    }

    def integer_to_roman(self, number):
        if not 1 <= number <= 3999:
            raise ValueError("Number must be between 1 and 3999")

        roman = []
        for value, symbol in self.values:
            while number >= value:
                roman.append(symbol)
                number -= value
        return "".join(roman)

    def roman_to_integer(self, roman_numeral):
        total = 0
        previous_value = 0

        for symbol in reversed(roman_numeral.upper()):
            current_value = self.roman_map[symbol]
            if current_value < previous_value:
                total -= current_value
            else:
                total += current_value
                previous_value = current_value
        return total


class WordReverser:
    def reverse_words(self, text):
        words = text.split()
        return " ".join(reversed(words))


if __name__ == "__main__":
    converter = RomanNumeralConverter()

    number = 1994
    roman_value = converter.integer_to_roman(number)
    print(f"Integer to Roman: {number} -> {roman_value}")

    roman_input = "MCMXCIV"
    integer_value = converter.roman_to_integer(roman_input)
    print(f"Roman to Integer: {roman_input} -> {integer_value}")

    reverser = WordReverser()
    input_string = "hello world"
    output_string = reverser.reverse_words(input_string)
    print(f"Input string : '{input_string}'")
    print(f"Expected Output : '{output_string}'")
