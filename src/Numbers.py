import japanese_numbers
import millify


number_names = ["", " million", " billion", " trillion", " quadrillion", " quintillion", " sextillion"]

def convert(number):
    number = convert_number_chars(number)
    arabic = japanese_numbers.to_arabic(number)[0].number
    english = millify.millify(arabic, precision=10, prefixes=number_names)
    return english


# the library used cannot parse the full width Japanese numbers
def convert_number_chars(nr):
    return "".join([number_normal_writing(c) for c in nr])


def number_normal_writing(c):
    return {
        "１": "1",
        "２": "2",
        "３": "3",
        "４": "4",
        "５": "5",
        "６": "6",
        "７": "7",
        "８": "8",
        "９": "9",
        "０": "0",
    }.get(c,c)


def number_japanese_writing(c):
    return {
        "1": "１",
        "2": "２",
        "3": "３",
        "4": "４",
        "5": "５",
        "6": "６",
        "7": "７",
        "8": "８",
        "9": "９",
        "0": "０",
    }.get(c,c)
