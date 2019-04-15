from util import english_alphabet
# for transforming a letter to binary representation
import binascii
# for splitting a long string in even parts
from textwrap import wrap

def letter_to_binary(letter):
    # converts a letter to its binary representation
    return str(bin(int.from_bytes(letter.encode(), 'big') - 1 ))[4:]

def text_to_binary(text):
    out = ""
    for letter in text:
        out += letter_to_binary(letter)
    return out

def letter_from_binary(binary):
    # converts to a letter from binary
    binary_str = "0b"+binary
    number = int(binary_str,2)
    return english_alphabet[number]

def binary_to_string(binary_string):
    # converts a binary string to a letter string
    binary_split = wrap(binary_string,5)

    letter_list = []

    for binary in binary_split:
        letter = letter_from_binary(binary)
        letter_list.extend([letter])
    return "".join(letter_list)

def LFSR1(key): # matches geffe in 3/4 cases
    return (key[1] + key[4]) % 2
def LFSR2(key): # matches geffe in 1/2 cases
    return (key[0] + key[6]) % 2
def LFSR3(key): # matches geffe in 3/4 cases
    return (key[1] + key[10]) % 2

def geffe(key1,key2,key3):
    # geffe generator, generates the next bit, based on current key
    x1 = LFSR1(key1)
    key1.insert(0,x1)

    x2 = LFSR2(key2)
    key2.insert(0,x2)
    
    x3 = LFSR3(key3)
    key3.insert(0,x3)
    return (x1 * x2 + x2 * x3 + x3) % 2

def decript(input,key1,key2,key3):
    decripted = []

    for bit in input:
        geffe_bit = geffe(key1,key2,key3)
        decripted.extend([(bit + geffe_bit)%2])
    return "".join(decripted)

def decript_with_LFSR(input,LFSR_fun, key):
    key = list(key)
    #print("key: " + str(key))

    decripted = []
    for bit in input:
        LFSR_bit = LFSR_fun(key)
        newKey = [LFSR_bit]
        newKey.extend(key)
        key = newKey
        decripted.extend([str((int(bit) + int(LFSR_bit))%2)])
    return "".join(decripted)

def increase_key(key):
    for i in range(len(key)):
        if key[i] == 0:
            key[i] = 1
            return (True,key)
        key[i] = 0
    return (False,0)

def check_similarity(known_text,cipher):
    #print("cipher: " + str(cipher))
    #print()
    correct = 0
    for i in range(len(known_text)):
        if known_text[i] == cipher[i]:
            correct += 1
    return correct * 1.0 / len(known_text)

def brute_force_LFSR(known_text,cipher_text,LFSR_fun = LFSR3,min_key_length = 11):
    """
    find the key for specified LFSR, we can do this using a correlation attack if we have some known plaintext
    around 50% similarity is expected due to randomness, however higher values mean that the key for this LFSR
    is probably the one used in the geffe generator
    """
    cipher_text = cipher_text[:len(known_text)]

    for key_length in range(min_key_length,20):
        print("key length " + str(key_length))
        key = [0 for i in range(key_length)]

        increased = True
        while(increased):
            out = decript_with_LFSR(list(cipher_text),LFSR_fun,key)
            similarity = check_similarity(known_text,out)
            #print(key,similarity)
            if similarity > 0.7:
               print(key,similarity)
               return
            increased,key = increase_key(key)



if __name__ == "__main__":
    KRIPTO = "01100111011111111001100011111010101011100111101100011111100100111000111010010110111110110110111010000000011000100110111011001110000110010111010010011000101110001000000101011101011101011110111111110110110111001000100000100011101000000011110010110110100011100101100100111011011111011000100010111010110011101001001111100100100011000111011110001001011111010110011101010011010111010010000010000001000100001101010111010011100100011111010111111011100011000011000001111000101110100110101100011111000110010011100010101100011110101001101000101010101001001111111101101110110111010010110010010111100111111110000000010001010011101000001010010101111000111101100000000111111111010100111010010000110011000111111101011010001001110101101010101101101100101101011101000010011111110010001010101000101011111101110000100101110001110111010011101101110011000111000110000001010111101100000011000111100110101100111010000000111010110111101110000001010100110111000010001111000001110110100000101110010101111110001110010101000100100011000010010100001100001111010110101001111111100110010110110010010000001000110000011010101010100011010111100011100011100001011110111110110111010100010100001010101111101111010011011010101111011111110100100010110110111001101100010100001101101000111100111011101011110010001011010001110000000111000011010011000111000101011100101100001011100011011110110001100001000111011101010101011010101011100100110010001111110001011000011011000100011111001100100110110001100110001000100101100101101010010100010011001111111101010001000111110110100011000000001011000000001101111001000000011011000011001001000001000001100010100110100101111001010101100110111011111001100100101101011110011011101100010110111100110100111110000010000101100011010111000000100111110100111011110001101001011000010101111111001111010001000101001110110000000101001111011010010011010100001101110000110011010101001001011100100110100010010011010111100101110001110000110111001011100100011100101111110111100110111111011110111110111101110010111000101001011101011000110011111011001000110001101010110100100011011010000110011111101000010010111010111010110000010011010000011110111100101110010010001100001010110110100101111000011001011101100010100011111001001011010101111111010101010110101000100101011011110000111100000101011100011110010000110010100000010100100011001000000100101010000011110111000100111010011000100000111001001011000011001011010100001010000001101111001001100100011101111001111101000010011010011111100110001111111011100101111000101010111000110010001000011010011101100000001101010000001101101000100111101000001110111001110100101110001100001110111110101110101111011110000010001100111101101011100101011000001101010101010110000111100010101101011110001000010001111100100101110110110010011110110010011001010001101100101011000001011101010001010110000010101111111100000111100111110010111101001010110000000100101000101111110111011110101110101010111100101000111101000101011000101100110000010000011010101000011001101110111110100111011111011001101001011001100000111011101110"
    KNOWNTEXT = "CRYPTOGRAPHY"
    KNOWN_BIN = "000101000111000011111001101110001101000100000011110011111000"

    """
    Attacking geffe generator with correlation attack using plaintext. I split the LFSR's to attack them individually.
    Because 2 of the 3 LFSR's have a high correlation with the geffe generator I can exploit this. I will attack them seperately.

    LFSR1 and LFSR3 have a 75% correlation, if I get a key that decripts to plaintext that is around 75% similar to the plaintext sample
    I can expect the key to be the correct one

    I got the minimum key length from looking at the LFSR polynome.
    """
    brute_force_LFSR(KNOWN_BIN,KRIPTO,LFSR1,5) # returns [1, 0, 1, 0, 0] 0.7666666666666667
    brute_force_LFSR(KNOWN_BIN,KRIPTO,LFSR3,11) # [1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0] 0.7333333333333333

    """
    Using the function brute_force_LFSR(known_text,cipher_text,LFSR_fun = LFSR3,min_key_length = 11), and using LFSR1,
    I found out that it's key is [1, 0, 1, 0, 0] with 0.7666666666666667 confidence.

    similarely for LFSR3
    """