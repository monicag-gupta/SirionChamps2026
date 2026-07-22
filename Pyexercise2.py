class ReverseString:

    def reverse_words(self, text):
        words = text.split()      # Split string into words
        words.reverse()           # Reverse the list of words
        return " ".join(words)    # Join words back into a string


# Driver Code
obj = ReverseString()

text = input("Enter a string: ")
print("Reversed string:", obj.reverse_words(text))