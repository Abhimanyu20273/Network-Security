#plaintext, 128 bits
#key, 128 bits
from random import randint 
import numpy as np
Char_Int_Dict = {}
Int_Char_Dict = {}
for i in range(10):
    Int_Char_Dict[i] = str(i)
    Char_Int_Dict[str(i)] = i
val = 10
for alphabet in "ABCDEF":
	Char_Int_Dict[alphabet] = val
	Int_Char_Dict[val] =  alphabet
	val+=1




def convert_to_matrix(myString,matrix):
	byte_values = myString.split()
	count = 0
	for i in range(4):
		row = []
		for j in range(4):
			row.append(byte_values[count])
			count = count + 1
		matrix.append(row)
	return matrix
def convert_hex_int(mystring):
	first_val = Char_Int_Dict[mystring[0]]
	second_val = Char_Int_Dict[mystring[1]]
	value = first_val * 16 + second_val
	return value
def convert_int_hex(num):
	value = 0
	if(num < 16) :
		value = "0" + hex(num)[2].upper()
	else:
		value = hex(num)[2].upper() + hex(num)[3].upper()
	return value
def Hex_Int_func_matrix(state_matrix):
	new_matrix = []
	for i in range(4):
		row = []
		for j in range(4):
			value = convert_hex_int(state_matrix[i][j])
			# print("first val {} second val {}, array val {} final value {}".format(first_val,second_val,state_matrix[i][j],value))
			row.append(value)
		new_matrix.append(row)
	return new_matrix

def Int_Hex_func_matrix(state_matrix):
	new_matrix = []
	for i in range(4):
		row = []
		for j in range(4):
			value = state_matrix[i][j]
			if(value < 16) :
				row.append("0" + hex(state_matrix[i][j])[2].upper())
			else:
				row.append(hex(state_matrix[i][j])[2].upper() + hex(state_matrix[i][j])[3].upper())
		new_matrix.append(row)
	return new_matrix

sbox = []
for i in range(16):
	row = []
	for j in range(16):
		row.append(convert_int_hex(randint(0,255)))
	sbox.append(row)

matrix_MC = []
for i in range(4):
	row = []
	for j in range(4):
		row.append(randint(0,255))
	matrix_MC.append(row)

RC_hex = ["01","02","04","08","10","20","40","80","1B","36"]
RCs = []
for i in range(10):
	RCs.append(convert_hex_int(RC_hex[i]))

def add_round_key(state_matrix,key):
	for i in range(4):
		for j in range(4):
			state_matrix[i][j] = state_matrix[i][j] ^ key[i][j]
	return state_matrix
def substitute_bytes(state_matrix):
	for i in range(4):
		for j in range(4):
			xy = state_matrix[i][j]
			x = Char_Int_Dict[xy[0]]
			y = Char_Int_Dict[xy[1]]
			state_matrix[i][j] = sbox[x][y]
	return state_matrix
def shift_rows(state_matrix):
	new_matrix = []
	new_matrix.append(state_matrix[0])

	for k in range(1,4):
		row = []
		for i in range(4):
			j = i + k
			if(j > 3):
				j = j%4
			row.append(state_matrix[k][j])
		new_matrix.append(row)
	return new_matrix

def mix_column(state_matrix):
	new_matrix = np.matmul(matrix_MC,state_matrix)
	for i in range(4):
		for j in range(4):
			new_matrix[i][j] = new_matrix[i][j] % 256
	return new_matrix

def key_expansion(key_matrix,RC_num):
	row = []
	for i in range(4):
		j = i + 1
		if(j > 3):
			j = j%4
		row.append(key_matrix[0][j])
	for j in range(4):
		x = Char_Int_Dict[row[j][0]]
		y = Char_Int_Dict[row[j][1]]
		row[j] = sbox[x][y]


	RC_arr = [RCs[RC_num],0,0,0]
	key_matrix = Hex_Int_func_matrix(key_matrix)
	output_row = []
	for i in range(4):
		output_row.append(convert_hex_int(row[i]) ^ RC_arr[i])

	new_matrix = []
	new_matrix.append(output_row)
	output_row = []

	for k in range(3):
		for i in range(4):
			output_row.append(new_matrix[k][i] ^ key_matrix[k + 1][i])
		new_matrix.append(output_row)
		output_row = []
	return new_matrix

plaintext = "0F 1D 29 3C 4B 6E 98 54 0F 1D 29 3C 4B 6E 98 54"
state_matrix = []
state_matrix = convert_to_matrix(plaintext,state_matrix)

# state_matrix = Int_Hex_func_matrix(state_matrix)
# print(state_matrix)
dummy_key = "01 18 29 3D 44 65 95 53 1F 24 26 4C 46 34 56 AE"
key_matrix = convert_to_matrix(dummy_key,[])


#Add round key
state_matrix = Hex_Int_func_matrix(state_matrix)
key_matrix = Hex_Int_func_matrix(key_matrix)
state_matrix = add_round_key(state_matrix,key_matrix)

for m in range(10):
	#Substitute bytes
	state_matrix = Int_Hex_func_matrix(state_matrix)
	# print(state_matrix)
	state_matrix = substitute_bytes(state_matrix)
	# print(state_matrix)

	#Shift rows
	state_matrix = shift_rows(state_matrix)

	#Mix columns
	state_matrix = Hex_Int_func_matrix(state_matrix)
	# print(state_matrix)
	state_matrix = mix_column(state_matrix)
	# print(state_matrix)

	#Key expansion
	key_matrix = Int_Hex_func_matrix(key_matrix)
	key_matrix = key_expansion(key_matrix,m)


	#Add round key
	state_matrix = add_round_key(state_matrix,key_matrix)
	# print(state_matrix)

state_matrix = Int_Hex_func_matrix(state_matrix)
output_cipher = ""
for i in range(4):
	for j in range(4):
		output_cipher = output_cipher + state_matrix[i][j] + " "

print("The output cipher is {}".format(output_cipher))


