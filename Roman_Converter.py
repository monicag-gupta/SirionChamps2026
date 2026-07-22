class RomanConverter:

    def int_to_roman(self, number):
        # Matching list of values and their Roman symbols from largest to smallest
        number_values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        roman_symbols = [
            "M",
            "CM",
            "D",
            "CD",
            "C",
            "XC",
            "L",
            "XL",
            "X",
            "IX",
            "V",
            "IV",
            "I",
        ]

        roman_result = ""
        position = 0

        # Keep taking away the largest possible value
        while number > 0:
            if number >= number_values[position]:
                roman_result += roman_symbols[position]
                number -= number_values[position]
            else:
                position += 1  # Move to the next smaller value

        return roman_result

    def roman_to_int(self, roman_text):
        # Basic value of each Roman letter
        letter_values = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

        # Make sure input is uppercase so "mcmxciv" also works
        roman_text = roman_text.upper()
        total_score = 0

        for current_position in range(len(roman_text)):
            current_letter_value = letter_values[roman_text[current_position]]

            # Check if there is a next letter and if it's larger (like IV)
            if (
                current_position + 1 < len(roman_text)
                and letter_values[roman_text[current_position + 1]]
                > current_letter_value
            ):
                total_score -= current_letter_value
            else:
                total_score += current_letter_value

        return total_score


# Create our converter tool
converter = RomanConverter()

# --- ASK USER FOR INPUT ---
print("--- Roman Numeral Converter ---")
print("1. Convert Number to Roman")
print("2. Convert Roman to Number")

choice = input("Enter 1 or 2: ")

if choice == "1":
    user_number = int(input("Enter a whole number (e.g., 1994): "))
    result = converter.int_to_roman(user_number)
    print(f"The Roman numeral for {user_number} is: {result}")

elif choice == "2":
    user_roman = input("Enter a Roman numeral (e.g., MCMXCIV): ")
    result = converter.roman_to_int(user_roman)
    print(f"The number for {user_roman.upper()} is: {result}")

else:
    print("Invalid choice! Please run the program again and select 1 or 2.")