class ReverseString:
    def __init__(self, text):
        self.text = text

    def reverse_words(self):
        words = self.text.split()
        reversed_words = words[::-1]
        return " ".join(reversed_words)


if __name__ == "__main__":
    input_string = input("Enter a string: ")
    obj = ReverseString(input_string)
    result = obj.reverse_words()
    print("Reversed string:", result)
