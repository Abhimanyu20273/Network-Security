import hashlib
import requests

from RSA_cryptosystem import encrypt

registrar_credentials = {
	'Public_key': '5282963831,1343',
	'Private_key': '5282963831,641176031'
}
director_credentials = {
	'Public_key': '5060330447,3149',
	'Private_key': '5060330447,702223637'
}

# Get the current UTC time using the API of worldtimeapi.org
# This is a reliable source of current time
# The request is https which ensures encryption for security
def get_UTC_time():
	response = requests.get('https://worldtimeapi.org/api/timezone/Etc/UTC')
	if response.status_code == 200:
		timestamp = response.json().get('datetime','Missing timestamp')
	else:
		timestamp = 'Missing timestamp'
	return timestamp


# Generate the SHA256 hash of a byte encoded message and then convert it to hexadecimal
# First the SHA256 generated and then its hexadecimal version is generated
def gen_hash(message):
	hex_hash = hashlib.sha256(message).hexdigest()
	print(f'Hash: {hex_hash}')
	return hex_hash

# Generate the hash for an input file concatenated with the contents of a message
def gen_hash_file_and_message(fileName, registrarSignature = ''):
	with open(fileName, 'rb') as f:
	    fileContents = f.read()
	fileContentsPlusMessage = fileContents + registrarSignature.encode('utf-8')
	return gen_hash(fileContentsPlusMessage)

# Generate the digital signature using the following steps:
# 1. Read the file as a byte string 
# 2. If the registrar's signature is recevied as input, byte encode it and concatenate it to the read file byte string
# 3. Genarate an SHA256 hash for the above byte string
# 4. Securely get the current time and concatenate it to the hash
# 5. Encrypt the string from step 3 using the private key of the registrar or director
def generate_signature(fileName, registrarSignature = ''):
	hash = gen_hash_file_and_message(fileName, registrarSignature)
	timestamp = get_UTC_time()
	hashPlusTimeStamp = f'{hash}||{timestamp}'
	print(f'hashPlusTimeStamp = {hashPlusTimeStamp}')
	if registrarSignature:
		# If the registrar's signature is supplied, then we need to generate the Director's signature.
		# So use Director's private key, else use the Registrar's key.
		privateKey = director_credentials['Private_key']
	else:
		privateKey = registrar_credentials['Private_key']
	signature = encrypt(hashPlusTimeStamp, privateKey)
	print(f'Signature = {signature}')
	return signature




if __name__ == '__main__':
	message = 'Abhimanyu Bhatnagar'
	fileName = 'pdfs/watermarkedDegree_Abhishek_Jain_232023.pdf'
	print(gen_hash_file_and_message(fileName, message))