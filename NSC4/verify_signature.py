# Verify digital signatures
import hashlib
import requests

from RSA_cryptosystem import decrypt

pkda_public_key = '5501485559,3109'

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

# Get the public key of registrar or director from the PKDA
def get_public_key_from_pkda(client):
	response = requests.get(f'http://127.0.0.1:5002/get_public_key?client_id={client}')
	if response.status_code == 200:
		encrypted_public_key = response.json().get('encrypted_public_key','')
		public_key = decrypt(encrypted_public_key, pkda_public_key)
		return public_key
	else:
		return 'Client not found'


if __name__ == '__main__':
	# Collect inputs from the user for verification
	downloadedFileName = input("Enter the file path of the downloaded file: ")
	registrarSignature = input("Enter the registrar's digital signature: ")
	directorSignature = input("Enter the director's digital signature: ")

	registrar_public_key = get_public_key_from_pkda('registrar')
	director_public_key = get_public_key_from_pkda('director')
	print()
	print("Obtained Registrar and Director's public keys from PKDA")
	print()

	# Decrypt the registrar's signature using registrar_public_key
	print("Decrypting the registrar's signature using registrar's public key")
	decryptedRegistrarString = decrypt(registrarSignature, registrar_public_key)
	registrarHash = decryptedRegistrarString.split('||')[0]
	registrarTimestamp = decryptedRegistrarString.split('||')[1]
	print(f'Registrar Hash = {registrarHash}')
	print(f'Registrar Timestamp = {registrarTimestamp}')
	print()
	# Generate hash for the downloaded file
	print('Generating the hash for the downloaded file')
	fileHash = gen_hash_file_and_message(downloadedFileName)
	if fileHash != registrarHash:
		print('Mismatch in registrar signature.')
	else:
		print('Generated hash matched the registrar hash.')
	print()

	# Decrypt the director's signature using director_public_key
	print("Decrypting the director's signature using director's public key")
	decryptedDirectorString = decrypt(directorSignature, director_public_key)
	directorHash = decryptedDirectorString.split('||')[0]
	directorTimestamp = decryptedDirectorString.split('||')[1]
	print(f'Director Hash = {directorHash}')
	print(f'Director Timestamp = {directorTimestamp}')
	print()

	# Generate hash for the file and registrar's signature
	print("Generating the hash for the downloaded file || registrar's signature")
	fileHash = gen_hash_file_and_message(downloadedFileName, registrarSignature)
	if fileHash != directorHash:
		print('Mismatch in director signature.')
	else:
		print('Generated hash matched the director hash. Verification completed')
