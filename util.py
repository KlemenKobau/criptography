english_alphabet = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P",
                    "Q","R","S","T","U","V","W","X","Y","Z")
letter_frequency = (0.08167,0.01492,0.02782,0.04253,0.12702,0.02228,0.02015,0.06094,
                    0.06966,0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507,
                    0.01929,0.00095,0.05987,0.06327,0.09056,0.02758,0.00978,0.02360,
                    0.00150,0.01974,0.00074)

def to_numbers(word):
    word = word.upper()
    numbers = []
    for char in word:
        numbers.extend([english_alphabet.index(char)])
    return numbers

def to_word(numbers):
    word = ""
    for number in numbers:
        word += english_alphabet[number]
    return word

if __name__ == "__main__":
    print(len(english_alphabet) == len(letter_frequency))
