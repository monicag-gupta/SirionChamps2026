class StringReverser:

    def reverse_words(self, text):
        # Step 1: Split the text into a list of individual words
        # 'hello world' becomes ['hello', 'world']
        word_list = text.split()

        # Step 2: Reverse the order of the words in the list
        # ['hello', 'world'] becomes ['world', 'hello']
        reversed_list = word_list[::-1]

        # Step 3: Join the words back together with spaces in between
        # ['world', 'hello'] becomes 'world hello'
        reversed_text = " ".join(reversed_list)

        return reversed_text


# Create our reverser tool
reverser = StringReverser()

# --- ASK USER FOR INPUT ---
print("--- Word Reverser ---")
user_input = input("Enter a sentence (e.g., 'hello world'): ")

# Convert and display result
output_text = reverser.reverse_words(user_input)
print(f"Reversed output: '{output_text}'")