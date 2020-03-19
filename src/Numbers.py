import japanese_numbers
import millify


number_names = ["", " million", " billion", " trillion", " quadrillion", " quintillion", " sextillion"]

def convert(number):
    arabic = japanese_numbers.to_arabic(number)[0].number
    english = millify.millify(arabic, precision=10, prefixes=number_names)
    return english



