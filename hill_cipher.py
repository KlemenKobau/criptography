import math,copy
from util import to_numbers,to_word,english_alphabet
from vigener_cipher import chi_squared

def reshape(num_word,key_length):
    mat_word = [[-1 for i in range(key_length)] for j in range( math.ceil(len(num_word) / float(key_length)))]

    for i in range(len(mat_word[0]) * len(mat_word)):
        if(i >= len(num_word)):
            mat_word[i//key_length][i%key_length] = 0
        else:
            mat_word[i//key_length][i%key_length] = num_word[i]
    return mat_word

def multiply(vector_word,mat_key):
    vec_res = [0 for i in range(len(vector_word))]

    for i in range(len(mat_key[0])):
        for j in range(len(mat_key)):
            vec_res[i] += vector_word[j] * mat_key[i][j]
        vec_res[i] = vec_res[i]%len(english_alphabet)
    
    return vec_res

def encript(mat_word,key):
    res = [0 for i in range(len(mat_word))]

    for i in range(len(res)):
        res[i] = multiply(mat_word[i],key)
    return res

def matrix_to_vector(mat_word):
    out = []
    for i in range(len(mat_word)):
        out.extend(mat_word[i])
    return out

def inc_key(key_mat):
    for i in range(len(key_mat)):
        for j in range(len(key_mat)):
            key_mat[i][j] += 1                
            if(key_mat[len(key_mat) - 1][len(key_mat) - 1] == len(english_alphabet)):
                return None
            if key_mat[i][j] == len(english_alphabet):
                key_mat[i][j] = 0
            else:
                return key_mat
    return key_mat

def find_key(mat_word):
    if type(mat_word) is str:
        mat_word = to_numbers(mat_word)
        mat_word = reshape(mat_word,2)
    key = [[0,0],[0,0]]
    test_word = copy.deepcopy(mat_word)

    min_score = 1000
    out_key = None
    top_decript = None

    while key != None:
        res = encript(test_word,key)
        num_res = matrix_to_vector(res)
        score = chi_squared(num_res)
        if(score < min_score):
            min_score = score
            out_key = copy.deepcopy(key)
            top_decript = num_res
        key = inc_key(key)
    return (out_key,top_decript)



if __name__ == "__main__":
    key = [[1,2],[7,9]]
    cipher = "STSQALWTCJMIJMTHNFEBWZTVJWMRNNHPMFICJFNWSZSXGWPFHHAJFBNTWZTVTHIRMRCGVRJTAFXBWDIVMFWSNSTVLXIRACANWLYSIYVPJQMQNFLNMRPXSBHMWNJTIYNSZNHPHPIMNZDRWBPPNSHMSBUJMUHZXJHMWPSQHHJBMHHMWMJTAFXBWDICVETVLXIRANXFVETVUDWUHBWHEBMBSXHMWEEEHMANWUJUWWHAWWSNWZMLJXVXHWTVJTZZICACHHJTNWWTZRHWWTIYJSSUWSNSTVLWWWWHHPNSTVSNWWIYNSSOPFHMWEWHMHHMWNJTIYNSXPCQJTOQYFPBQKHMWEWHMHHMWNACHRNWHMWBSZWSIOGIICVETVLWWWWHHXANZRVZYWXUMVWZHDJHXAANHRUQZZOUNBTZTJFNSBUUMBVZSTTLHZXNWDTZELTVPPAJWTICVETVNNHPMFVZYWXUTVXBAJSQIUWWMHHMWNACHTGCTJIRGFCGVGSBYAPQITSDWISVPPNNZMWCIRMSFRSXHMWZEENFGDVBMHSYOYJHPBHLANXNNZVOSUSANTCVTVUMPSIATHYFAHEGCSPBWKNZMFWUYFIKXBMHHMWAAZWGJJAHSSWKVJANANXFVMAFSENLHMWBLZNDHMSBUJMNALWUFRSXWDMFWSVBTHLLJTYOSQWHYAGJHDJTXNNSTVMXTVJH"
    word = to_numbers("helloksjiajs")
    word = reshape(word,len(key))
    res = encript(word,key)
    out = matrix_to_vector(res)
    out_fun = find_key(cipher)
    print(to_word(out_fun[1]))