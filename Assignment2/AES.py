#plaintext, 128 bits
#key, 128 bits
from random import randint 
import numpy as np

sbox = [
    ['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76'],
    ['CA', '82', 'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0'],
    ['B7', 'FD', '93', '26', '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15'],
    ['04', 'C7', '23', 'C3', '18', '96', '05', '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75'],
    ['09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52', '3B', 'D6', 'B3', '29', 'E3', '2F', '84'],
    ['53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39', '4A', '4C', '58', 'CF'],
    ['D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C', '9F', 'A8'],
    ['51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2'],
    ['CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73'],
    ['60', '81', '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB'],
    ['E0', '32', '3A', '0A', '49', '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79'],
    ['E7', 'C8', '37', '6D', '8D', 'D5', '4E', 'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08'],
    ['BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8', 'DD', '74', '1F', '4B', 'BD', '8B', '8A'],
    ['70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57', 'B9', '86', 'C1', '1D', '9E'],
    ['E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55', '28', 'DF'],
    ['8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16']
]

inv_s_box = [
    ['52', '09', '6A', 'D5', '30', '36', 'A5', '38', 'BF', '40', 'A3', '9E', '81', 'F3', 'D7', 'FB'],
   [ '7C', 'E3', '39', '82', '9B', '2F', 'FF', '87', '34', '8E', '43', '44', 'C4', 'DE', 'E9', 'CB'],
   [ '54', '7B', '94', '32', 'A6', 'C2', '23', '3D', 'EE', '4C', '95', '0B', '42', 'FA', 'C3', '4E'],
   [ '08', '2E', 'A1', '66', '28', 'D9', '24', 'B2', '76', '5B', 'A2', '49', '6D', '8B', 'D1', '25'],
   [ '72', 'F8', 'F6', '64', '86', '68', '98', '16', 'D4', 'A4', '5C', 'CC', '5D', '65', 'B6', '92'],
   [ '6C', '70', '48', '50', 'FD', 'ED', 'B9', 'DA', '5E', '15', '46', '57', 'A7', '8D', '9D', '84'],
   [ '90', 'D8', 'AB', '00', '8C', 'BC', 'D3', '0A', 'F7', 'E4', '58', '05', 'B8', 'B3', '45', '06'],
   [ 'D0', '2C', '1E', '8F', 'CA', '3F', '0F', '02', 'C1', 'AF', 'BD', '03', '01', '13', '8A', '6B'],
   [ '3A', '91', '11', '41', '4F', '67', 'DC', 'EA', '97', 'F2', 'CF', 'CE', 'F0', 'B4', 'E6', '73'],
   [ '96', 'AC', '74', '22', 'E7', 'AD', '35', '85', 'E2', 'F9', '37', 'E8', '1C', '75', 'DF', '6E'],
   [ '47', 'F1', '1A', '71', '1D', '29', 'C5', '89', '6F', 'B7', '62', '0E', 'AA', '18', 'BE', '1B'],
   [ 'FC', '56', '3E', '4B', 'C6', 'D2', '79', '20', '9A', 'DB', 'C0', 'FE', '78', 'CD', '5A', 'F4'],
   [ '1F', 'DD', 'A8', '33', '88', '07', 'C7', '31', 'B1', '12', '10', '59', '27', '80', 'EC', '5F'],
   [ '60', '51', '7F', 'A9', '19', 'B5', '4A', '0D', '2D', 'E5', '7A', '9F', '93', 'C9', '9C', 'EF'],
   [ 'A0', 'E0', '3B', '4D', 'AE', '2A', 'F5', 'B0', 'C8', 'EB', 'BB', '3C', '83', '53', '99', '61'],
   [ '17', '2B', '04', '7E', 'BA', '77', 'D6', '26', 'E1', '69', '14', '63', '55', '21', '0C', '7D']
]
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

def int_bin(num):
	bin_string = bin(num)[2:]
	while(len(bin_string) != 8):
		bin_string = "0" + bin_string
	return bin_string

def multiplication_GF28(num1,num2):
	binary1 = int_bin(num1)
	binary2 = int_bin(num2)
	result = 0
	mod_val = 283
	for i in range(7,-1,-1):
		if(binary1[i] == "1"):
			result = result ^ num2
		num2 = num2 << 1
		if(binary2[0] == "1"):

			num2 = num2 ^ mod_val
		binary2 = int_bin(num2)
	return result

def multiply_rows(row1,row2):
	return multiplication_GF28(row1[0],row2[0]) ^ multiplication_GF28(row1[1],row2[1]) ^ multiplication_GF28(row1[2],row2[2]) ^ multiplication_GF28(row1[3],row2[3])

def mix_column(state_matrix):
	new_matrix = []
	for i in range(4):
		row = []
		for j in range(4):
			row.append(multiply_rows(matrix_MC[j],state_matrix[i]))
		new_matrix.append(row)
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


#Decryption Function:
character_int_value = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15, 'a':10, 'b':11, 'c':12, 'd':13, 'e':14, 'f':15}

def calculate_xor(list1,list2):
  xor_values = ['','','','']
  for i in range(0,len(list1)):
    a_1 = '0x' + list1[i] #Converting into hexa
    i_1 = int(a_1,16)
    a_2 = '0x' + list2[i]
    i_2 = int(a_2,16)
    a_3 = hex(i_1 ^ i_2)
    xor_values[i] = a_3[2:]
  return xor_values

def addRound_key(list1,list2):
  result = [[],[],[],[]]
  for i in range(0,4):
    result[i] = calculate_xor(list1[i], list2[i]) #Calculating XOR of key and the input text
  return result

overflow_value = 0x100
modulus_value = 0x11B

def gf28_multiply(a1, b1) :
    sum_value = 0
    while (b1 > 0) :
        if (b1 & 1) :
          sum_value = sum_value ^ a1        
        b1 = b1 >> 1                      
        a1 = a1 << 1                          
        if (a1 & overflow_value) :
          a1 = a1 ^ modulus_value   
    return sum_value

def inverse_substitution_bytes(list1):
  for i in range(0, len(list1)):
    for j in range(0, len(list1[i])):
      if (len(list1[i][j]) == 1):
        list1[i][j] = '0'+list1[i][j]
      s = list1[i][j]
      c_0 = character_int_value[s[0]]
      c_1 = character_int_value[s[1]]
      value = inv_s_box[c_0][c_1] #Substituting the values from Inverse S Box
      list1[i][j] = value
  return list1

def right_shift_rows(string_matrix):
  result = [['','','',''],['','','',''],['','','',''],['','','','']]
  for i in range(0,len(string_matrix)):
    current_row = string_matrix[i]
    for j in range(0,len(current_row)):
      result[i][j]=string_matrix[i][(j-i)%4] #Shifting the 2nd,3rd and 4th rows right by 1,2,3 bytes respectively
  return result

inverse_mix_columns_matrix = [[14,11,13,9],[9,14,11,13],[13,9,14,11],[11,13,9,14]]

def inverse_mix_Columns(state):
  result = [['','','',''],['','','',''],['','','',''],['','','','']]
  result_mat = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]
  for i in range(0,len(state)):
    for j in range(0, len(state[i])):
      for k in range(0,len(state)):
        value_1 = '0x'+state[k][j]
        value_1 = int(value_1,16)
        result_mat[i][j] ^= gf28_multiply(inverse_mix_columns_matrix[i][k],value_1) #Multiplying the matrices in GF(2^8)

  for i in range(0,len(state)):
    for j in range(0,len(state[i])):
      result[i][j] = str(hex(result_mat[i][j]))[2:]
  # print(result)
  return result

hexadecimal_to_char = {'0':'A', '1':'B', '2':'C', '3':'D', '4':'E', '5':'F', '6':'G', '7':'H', 
                '8':'I', '9':'J', 'A':'K', 'B':'L', 'C':'M', 'D':'N', 'E':'O', 'F':'P', 
                '10':'Q', '11':'R', '12':'S', '13':'T', '14':'U', '15':'V', '16':'W', '17':'X',
                '18':'Y','19':'Z','a':'K', 'b':'L', 'c':'M', 'd':'N', 'e':'O', 'f':'P',}
def convert_to_plain(final_state):
	output_cipher = ""
	for i in range(4):
		for j in range(4):
			output_cipher = output_cipher + final_state[i][j] + " "
	return output_cipher

def Decryption(ciphertext,subkey):
  original_state = [['','','',''],['','','',''],['','','',''],['','','','']]
  for i in range(0,16):
    original_state[int(i%4)][int(i/4)] = hex(ord(ciphertext[i]))[2:]


  intermediate_states = []

  #Round 10
  state_1 = addRound_key(subkey[10],original_state) #Subkeys of round 10 - Used in reverse order
  state_2 = right_shift_rows(state_1)
  state_3 = inverse_substitution_bytes(state_2)
  print("Round 1: "+str(state_3))
  intermediate_states.append(state_3)

  #Round 9-1
  for round in range(9,0,-1):
    state_1 = addRound_key(subkey[round],intermediate_states[-1])
    state_2 = inverse_mix_Columns(state_1)
    state_3 = right_shift_rows(state_2)
    state_4 = inverse_substitution_bytes(state_3)
    print("Round "+str(11-round)+" :"+str(state_4))
    intermediate_states.append(state_4)
  
  #Round 0
  round0_key = subkey[0]
  round0_state = addRound_key(round0_key, intermediate_states[-1])
  print("Round 0: "+str(round0_state))
  intermediate_states.append(round0_state) 

  plain_text = convert_to_plain(intermediate_states[-1])
  print("Decrypted Plain Text: "+ plain_text)
  return plain_text, intermediate_states[-1], intermediate_states


if __name__ == '__main__':
	# matrix_MC = []
	# for i in range(4):
	# 	row = []
	# 	for j in range(4):
	# 		row.append(randint(0,255))
	# 	matrix_MC.append(row)
 
	matrix_MC = [[2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]]

	RC_hex = ["01","02","04","08","10","20","40","80","1B","36"]
	RCs = []
	for i in range(10):
		RCs.append(convert_hex_int(RC_hex[i]))

	plaintext = "0F 1D 29 3C 4B 6E 98 54 0F 1D 29 3C 4B 6E 98 54"
	state_matrix = []
	state_matrix = convert_to_matrix(plaintext,state_matrix)

	dummy_key = "01 18 29 3D 44 65 95 53 1F 24 26 4C 46 34 56 AE"
	key_matrix = convert_to_matrix(dummy_key,[])

	round_wise_keys = []
	round_wise_keys.append(key_matrix)
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
		round_wise_keys.append(Int_Hex_func_matrix(key_matrix))
		# print(state_matrix)

	state_matrix = Int_Hex_func_matrix(state_matrix)
	output_cipher = ""
	for i in range(4):
		for j in range(4):
			output_cipher = output_cipher + state_matrix[i][j] + " "

	print("The output cipher is {}".format(output_cipher))
 
	print("\nDecryption")
	print(round_wise_keys)
	plain_text, final_state, all_decrypted_states = Decryption(output_cipher,round_wise_keys)