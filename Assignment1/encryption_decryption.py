import string
from itertools import product

lowercase_letters = string.ascii_lowercase 
Char_Int_Dict = {}
Int_Char_Dict = {}
for i in range(len(lowercase_letters)):
    Int_Char_Dict[i] = lowercase_letters[i]
    Char_Int_Dict[lowercase_letters[i]] = i


def mapping_int_char(myArr):
    myString = ""
    for i in range(len(myArr)):
        myString += Int_Char_Dict[myArr[i]]
    return myString

def mapping_string_int(myString):
    myarr = []
    for i in range(len(myString)):
        myarr.append(Char_Int_Dict[myString[i]])
    return myarr
    
def hash_func(myString):
    myMatrix = []
    mappedValues = mapping_string_int(myString)
    arrLength = len(mappedValues)
    numLoops = arrLength // 8
    index = 0
    for i in range(numLoops):
        myMatrix.append(mappedValues[index:index + 8])
        index += 8
    if(arrLength % 8 !=0):
        new_arr = mappedValues[index:]
        while(len(new_arr) != 8):
            new_arr.append(0)
        myMatrix.append(new_arr)
    final_hash = [0 for i in range(8)]
    for i in range(len(myMatrix)):
        for j in range(8):
            final_hash[j] = final_hash[j] ^ myMatrix[i][j]
    hash_arr = [x%26 for x in final_hash]
    return mapping_int_char(hash_arr)

def poly_encryption(plaintext,hashstring,key):
    plain_text_arr = mapping_string_int(hashstring + plaintext)
    key_arr = mapping_string_int(key)
    new_arr = []
    key_index = 0
    key_len = len(key)
    for i in range(len(plain_text_arr)):
        new_arr.append((plain_text_arr[i] + key_arr[key_index]) % 26)
        key_index +=1
        key_index = key_index % key_len
    ciphertext = mapping_int_char(new_arr)
    return ciphertext

def poly_decryption(ciphertext,key):
   
    ciphertext_arr = mapping_string_int(ciphertext)
    key_arr = mapping_string_int(key)
    new_arr = []
    key_index = 0
    key_len = len(key)
    for i in range(len(ciphertext_arr)):
        new_arr.append((ciphertext_arr[i] - key_arr[key_index] + 26) % 26)
        key_index +=1
        key_index = key_index % key_len
    itermediate_plain = mapping_int_char(new_arr)
    plaintext = itermediate_plain[8:]
    hash_val = itermediate_plain[:8] 
    if(hash_val == hash_func(plaintext)):
        print("Successful decrypt")
        return plaintext
    else:
        # print("Failure")
        return None
    
def generate_string_combinations(length):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    combinations = [''.join(p) for p in product(alphabet, repeat=length)]
    return combinations

original_text = "wearediscoveredsaveyourselfover"
hash_value = hash_func(original_text)
sender_key = "decc"
ciphertext = poly_encryption(original_text,hash_value,sender_key)
print("\n-----Sender Space-----")
print("Original text: ",original_text)
print("Hash Value: ",hash_value)
print("key: ", sender_key)
receiver_key = "deca"
plaintext = poly_decryption(ciphertext,receiver_key)
print("\n-----Receiver Space-----")
print("Encrypted Text: ", ciphertext)
print("key: ",receiver_key)
if(plaintext==None):
    print("Failure to decrypt at key: ", receiver_key)
else:
    print("Plaintext: ", plaintext)

# Brute Force Attack
print("\n-----Attacker Space-----")
result = generate_string_combinations(4)
for i in result:
    if(poly_decryption(ciphertext,i)==None):
        continue
    else:
        print('key is ',i)
        break
    
