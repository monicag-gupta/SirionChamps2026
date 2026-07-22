class StringReverse:

    def reverse_words(self, text):
        words = text.split()
        return " ".join(words[::-1])


obj = StringReverse()

text = input("Enter a string: ")
print(obj.reverse_words(text))
