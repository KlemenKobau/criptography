from util import english_alphabet,to_numbers,to_word,letter_frequency

def encript(word, key):
    num_word = to_numbers(word)
    num_key = to_numbers(key)

    cipher = []

    for i in range(len(num_word)):
        cipher_num = (num_word[i] + num_key[i%len(num_key)]) % len(english_alphabet)
        cipher.extend([cipher_num])
    return to_word(cipher)

def decript(num_cipher,num_key):
    if type(num_cipher) is str:
        num_cipher = to_numbers(num_cipher)
    if type(num_key) is str:
        num_key = to_numbers(num_key)

    text = []

    for i in range(len(num_cipher)):
        text_num = num_cipher[i] - num_key[i%len(num_key)]

        if text_num < 0:
            text_num = len(english_alphabet) + text_num
        
        text.extend([text_num])
    return to_word(text)

def count_letters(num_word):
    num_occurences = [0 for i in range(len(english_alphabet))]

    for num in num_word:
        num_occurences[num] += 1
    return num_occurences

def index_of_coincidence(num_word):
    if type(num_word) is str:
        num_word = to_numbers(num_word)

    num_occurences  = count_letters(num_word)
    
    top = 0
    for occ in num_occurences:
        top += occ * (occ-1)
    
    bot = len(num_word) * (len(num_word) -1)

    return float(top)/bot

def split_word(num_word,key_length):
    split_word = [[] for i in range(key_length)]
    for i in range(len(num_word)):
        split_word[i%key_length].extend([num_word[i]])
    return split_word

def index_of_co_whole_word(num_word,key_length):
    if type(num_word) is str:
        num_word = to_numbers(num_word)
    
    splited_word = split_word(num_word,key_length)
    res = [0 for i in range(key_length)]

    for i in range(key_length):
        res[i] = index_of_coincidence(splited_word[i])
    return sum(res) / float(len(res))

def getKeyLength(num_word, max_key_length = 20, threshold = 0.06):
    if type(num_word) is str:
        num_word = to_numbers(num_word)
    
    out = []

    for i in range(1,max_key_length):
        res = index_of_co_whole_word(num_word,i)
        if res > threshold:
            out.extend([i])
           
    return out

def increaseKey(key):
    for i in range(len(key)-1,0-1,-1):
        key[i] += 1
        if(key[i] == len(english_alphabet) and i == 0):
            return None
        if(key[i] == len(english_alphabet)):
            key[i] = 0
        else:
            break
    return key

def chi_squared(num_word):
    if type(num_word) is str:
        num_word = to_numbers(num_word)
    
    count = count_letters(num_word)

    summ = 0
    for char_index in range(len(english_alphabet)):
        expected_num = letter_frequency[char_index] * len(num_word)
        top = (count[char_index] - expected_num)**2

        summ += top/expected_num
    
    return summ
    

def find_key_of_length(num_word,key_length):
    if type(num_word) is str:
        num_word = to_numbers(num_word)

    key = [0 for i in range(key_length)]
    splited = split_word(num_word,key_length)

    for i in range(len(key)):
        index_min = -1
        min_chi = 1000
        for letter_index in range(len(english_alphabet)):
            try_text = decript(splited[i],[letter_index])
            score = chi_squared(try_text)
            if(score < min_chi):
                min_chi = score
                index_min = letter_index
        key[i] = index_min
    return key

def findKey(num_word):
    if type(num_word) is str:
        num_word = to_numbers(num_word)
    candidates = getKeyLength(num_word)

    res = 1000
    key = None

    for candidate in candidates:
        key_cand = find_key_of_length(num_word,candidate)
        plain_text = decript(num_word,key_cand)
        score = chi_squared(plain_text)
        if(score < res):
            key = key_cand
            res = score
    return key


if __name__ == "__main__":
    enc = "UTAHELHUSBXLZAZYMVXXGELAUOGDTEMOQRTUKGHCQRGTQNMUATMVASMYANZMARMOQLBIQRMPQSHMUTLWQOISQCTUNELADOGNQNHBSHMVYABUFABUUTLLJILAQNVLUNZYQAMLYEKNQNVPQSHUFHBZBOBUFTALBRXZQNMYQBXSXIHUNRHBSHMVGRKLBUUSUCMVMSXCQRXAQSMHZDMOQPKLEIWLZTBHXEELOTBVZOVJGRKPZGBUDEZBXAKJAUKZQDNYUNZATEKLNEESUOGHPDXKZOMHXIMAXEMVFHXZFRTPZTALETKPREHMFHXLXEVAUOGPEBNATUFHZNTAGRXWDAVAUCTSXYTWBLBLPTHATEYHOTLPZTALOALL"
    print(decript(enc,findKey(enc)))