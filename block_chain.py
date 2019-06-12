import hashlib
import math
import gmpy2
import timeit

#Code used to find collisions

def find_coll():
    known_hashes = dict()

    for i in range(10000000000000000000000):
        to_hash = "mining_" + str(i)
        newH = hashlib.sha1(to_hash.encode('utf8')).hexdigest()
        best_part = newH[:11]
        if best_part in known_hashes:
            print("found match:")
            print(to_hash)
            print(known_hashes[best_part])
            break
        else:
            known_hashes[best_part] = to_hash

    # found collisions
    # mining_5603404
    # mining_4772222

# used for hashing text and turning it into a number
def hash_coll(text):
    hashed_text = hashlib.sha1(text.encode('utf8')).hexdigest()
    num = int(hashed_text,16)
    
    #print(num) # 653222382295586618370463671847145239723017395549
    return num

def get_q():
    q = pow(2,160)
    return gmpy2.next_prime(q)

# generating a prime p that satisfies q|p-1
def get_p(q):
    p = 179769313486231590772930519078902473361797697894230657273430081157732675805500963132708477322407536021120113879871393357658789768814416622492847430639474124377767893424865485276302219601246094119453082952085005768838150682342462881473913110540827237163350510684586298239947 * q + 1
    while p < pow(2,1024):
        p += q

    while not gmpy2.is_prime(p):
        p += q
    
    print(p)

    return p

# get alpha so that alpha = h^((p-1)/q) % p != 1
def get_alpha(q,p):
    h = 1500
    alpha = pow(h,(p-1)//q,p)
    while alpha == 1:
        h += 1
        alpha = pow(h,(p-1)//q,p)
    
    print(alpha)
    return alpha

# get beta so that beta = alpha^a % p 
def get_beta(p,alpha,a):
    beta = pow(alpha,a,p)
    print(beta)
    return beta

def get_gamma(alpha,k,p,q):
    gamma = pow(alpha,k,p) % q
    print(gamma)
    return gamma

def get_delta(k_inv,text_hash,a,gamma,q):
    delta = k_inv * (text_hash + a * gamma) % q
    print(delta)
    return delta

# function to find a pair of number and hash with 7 leading 0
def get_line4_hash_pair(line1,line2,line3):
    text_from_before =  line1 + "\n" + line2 + "\n" + line3
    numero = 0
    out = hashlib.sha1((text_from_before +"\n" +  str(numero)).encode('utf8')).hexdigest()
    while(out[:7] != "0000000"):
        numero += 1
        out = hashlib.sha1((text_from_before +"\n"+ str(numero)).encode('utf8')).hexdigest()
    print(numero,out)
    return (numero,out)


if __name__ == "__main__":
    text = "mining_5603404 mining_4772222" # got this with function find_coll()

    # generating signature
    q = 1461501637330902918203684832716283019655932542983 # get_q()
    p = 262733146001979837311819117676584403741148754051683951627100716112228456309970554914202208782049869930601066827747097294307099992826430365197764768180688657032444227863596740797543810286283780951037400786218357893002160283961712113287405730217366139147492742038047382821740109907129666758685576696574382556186271021827359 #get_p(q)

    alpha = 117626421380962333891590668035460601041008165717093730108169129338965269816998200964546892525583313899216344748851557154156928253080707088151499561865862516727082982593945002962686926535155818673290476584572741790163139668897244037444014571248888150339750001163258228328999666293130311268832272046861181014271902656533152 # get_alpha(q,p)
    a = 61054 # random number form random.org
    beta = 128641743312107219780703511433184265271501813425778678809162113495573133202496183977620761529062190140181554662097772965664683979436070854641226878187129403732169565027611131637373437079581648598427075356057894352570575338713464141291037575483316999571400453886380035518944273849961741525063157573043381906527031082378095 # get_beta(p,alpha,a)
    k = 534876 # another random number
    gamma = 1190888160076453145260900606073456224541153317353 #get_gamma(alpha,k,p,q)
    k_inv = pow(k,q-2,q) # can use this for inverse since q is prime https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
    delta = 80979435450559784928743639696785877668909291907 #get_delta(k_inv,hash_coll(text),a,gamma,q)
    # public key is (p,q,alpha,beta)

    # solution
    line1 = text + " " + str(653222382295586618370463671847145239723017395549) # the number is hashed collision
    line2 = "klemenkobau " + str(gamma) + " " + str(delta)
    line3 = "000000049723160ba5b04dd37cc521ff3a98bfe1" # hash from ziga
    #line4,line5 = get_line4_hash_pair(line1,line2,line3)
    line4 = 324895060
    line5 = "0000000b71c55fdc65377b1890a526b1d4c13580"
