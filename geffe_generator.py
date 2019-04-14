from util import english_alphabet
import binascii

def letter_to_binary(letter):
    # converts a letter to its binary representation
    return str(bin(int.from_bytes(letter.encode(), 'big') - 1 ))[4:]

def letter_from_binary(binary):
    binary_str = "0b"+binary
    number = int(binary_str,2)
    return english_alphabet[number]

if __name__ == "__main__":
    print(letter_from_binary(letter_to_binary("G")))
