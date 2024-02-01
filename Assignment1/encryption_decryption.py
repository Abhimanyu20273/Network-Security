import string
from itertools import product

lowercase_letters = string.ascii_lowercase 
Char_Int_Dict = {}
Int_Char_Dict = {}
for i in range(len(lowercase_letters)):
    Int_Char_Dict[i] = lowercase_letters[i]
    Char_Int_Dict[lowercase_letters[i]] = i
Char_Int_Dict['_'] = 26
Int_Char_Dict[26] = '_'

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
    hash_arr = [x%27 for x in final_hash]
    return mapping_int_char(hash_arr)

def poly_encryption(plaintext,hashstring,key):
    plain_text_arr = mapping_string_int(hashstring + plaintext)
    key_arr = mapping_string_int(key)
    new_arr = []
    key_index = 0
    key_len = len(key)
    for i in range(len(plain_text_arr)):
        new_arr.append((plain_text_arr[i] + key_arr[key_index]) % 27)
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
        new_arr.append((ciphertext_arr[i] - key_arr[key_index] + 27) % 27)
        key_index +=1
        key_index = key_index % key_len
    intermediate_plain = mapping_int_char(new_arr)
    plaintext = intermediate_plain[8:]
    hash_val = intermediate_plain[:8] 
    if(hash_val == hash_func(plaintext)):
        print("Successful decrypt")
        return plaintext
    else:
        return None
    
def generate_string_combinations(length):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    combinations = [''.join(p) for p in product(alphabet, repeat=length)]
    return combinations

file_path = 'input.txt'
output_text = ""
lines_list = []
with open(file_path, 'r') as file:
    for line in file:
        lines_list.append(line.strip())  
print(lines_list)

sentences = lines_list[:5]

sender_key = lines_list[5]
ciphertext_list = []
print("\n-----Sender Space-----")
output_text += f"\n-----Sender Space-----\n"
for i in sentences:
    original_text = i
    hash_value = hash_func(original_text)
    ciphertext = poly_encryption(original_text,hash_value,sender_key)
    print("Original text: ",original_text)
    print("Hash Value: ",hash_value)
    print("key: ", sender_key,"\n")
    output_text += f"Original text:  {original_text}\n"
    output_text += f"Hash Value:  {hash_value}\n"
    output_text += f"key:  {sender_key}\n\n"
    ciphertext_list.append(ciphertext)

receiver_key = lines_list[6]   
print("\n-----Receiver Space-----")
output_text += f"\n-----Receiver Space-----\n"
for i in ciphertext_list:
    plaintext = poly_decryption(i,receiver_key)
    print("Encrypted Text: ", i)
    print("key: ",receiver_key)
    output_text += f"Encrypted Text:  {i}\n"
    output_text += f"key:  {receiver_key}\n"
    if(plaintext==None):
        print("Failure to decrypt with : ", receiver_key,"\n")
        output_text += f"Failure to decrypt with :  {receiver_key}\n\n"
    else:
        print("Original Text: ", plaintext,"\n")
        output_text += f"Original Text:  {plaintext}\n\n"

# Brute Force Attack
print("\n-----Attacker Space-----")
output_text += f"\n-----Attacker Space-----\n"
keys = generate_string_combinations(4)
    
for key in keys:
    final_key_check = True
    for cipher in ciphertext_list:
        plaintext = poly_decryption(cipher, key)
        if(plaintext==None):
            final_key_check = False
            break
        else:
            print("Original Text: ",plaintext)
            print("key that was successful in decryption of a ciphertext: ", key, "\n")
            output_text += f"Original Text: {plaintext}\n"
            output_text += f"Key that was successful in decryption of a ciphertext: {key}\n\n"
            
    if(final_key_check == True):
        print("The correct key is : ", key, "\n")
        output_text += f"The correct key is: {key}\n\n"
        break

output_file_path = 'output.txt'
with open(output_file_path, 'w') as output_file:
    output_file.write(output_text)