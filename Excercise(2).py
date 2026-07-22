class ReverseWords:

    def reverse_string(self, text):
        words = text.split()
        words.reverse()
        return " ".join(words)


obj = ReverseWords()

text = "hello world"
print("Original String:", text)
print("Reversed String:", obj.reverse_string(text))