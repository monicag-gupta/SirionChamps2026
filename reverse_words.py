class ReverseString:

    def reverse_words(self, text):
        words = text.split()
        return " ".join(reversed(words))


obj = ReverseString()

text = input("Enter a string: ")
print("Reversed String:", obj.reverse_words(text))