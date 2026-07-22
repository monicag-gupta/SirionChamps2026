class RomanConverter:
    def int_to_roman(self, num):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4, 1
        ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV", "I"
        ]
        roman = ""
        i = 0
        while num > 0:
            for _ in range(num // val[i]):
                roman += syb[i]
                num -= val[i]
            i += 1
        return roman

    def roman_to_int(self, s):
        roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
        total = 0
        prev = 0
        for ch in reversed(s):
            if roman[ch] < prev:
                total -= roman[ch]
            else:
                total += roman[ch]
            prev = roman[ch]
        return total

obj = RomanConverter()
print(obj.int_to_roman(58))
print(obj.roman_to_int("LVIII"))
