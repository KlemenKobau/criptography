import hashlib
import math
import gmpy2

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

def hash_coll(text):
    hashed_text = hashlib.sha1(text.encode('utf8')).hexdigest()
    num = int(hashed_text,16)
    
    #print(num) # 653222382295586618370463671847145239723017395549
    return num

def find_hash_with70(text):
    i = 0
    while(True):
        hashed = hashlib.sha1((text + str(i)).encode('utf8')).hexdigest()
        if hashed[:7] == "0000000":
            print(i)
            return i
        i += 1

def get_q():
    q = pow(2,160)
    return gmpy2.next_prime(q)

# generating a prime q that satisfies q|p-q
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

def sign(thing_to_sign):
    

if __name__ == "__main__":
    text = "mining_5603404 mining_4772222"

    q = 1461501637330902918203684832716283019655932542983 # get_q()
    p = 262733146001979837311819117676584403741148754051683951627100716112228456309970554914202208782049869930601066827747097294307099992826430365197764768180688657032444227863596740797543810286283780951037400786218357893002160283961712113287405730217366139147492742038047382821740109907129666758685576696574382556186271021827359 #get_p(q)

    alpha = 117626421380962333891590668035460601041008165717093730108169129338965269816998200964546892525583313899216344748851557154156928253080707088151499561865862516727082982593945002962686926535155818673290476584572741790163139668897244037444014571248888150339750001163258228328999666293130311268832272046861181014271902656533152 # get_alpha(q,p)
    a = 61054 # random number form random.org
    beta = 128641743312107219780703511433184265271501813425778678809162113495573133202496183977620761529062190140181554662097772965664683979436070854641226878187129403732169565027611131637373437079581648598427075356057894352570575338713464141291037575483316999571400453886380035518944273849961741525063157573043381906527031082378095 # get_beta(p,alpha,a)

    # public key is (p,q,alpha,beta)

    line1 = text + " " + str(653222382295586618370463671847145239723017395549) # the number is hashed collision
    line2 = "klemenkobau " + 