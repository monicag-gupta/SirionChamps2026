class ReverseWords:
    def reverse(self, text):
        words = text.split()
        words.reverse()
        return " ".join(words)

obj = ReverseWords()
print(obj.reverse("hello world"))
