import zmq
import time
import random
from RSA_cryptosystem import generate_keys, encrypt, decrypt

pkda_id = 'pkda_id'
initiator_id = 'client_1'
responder_id = 'client_2'

pkda_public_key = '5501485559,3109'


def initiator():
    # Create a ZeroMQ connection to send requests and get responses from the PKDA server
    context = zmq.Context()
    socket_pkda = context.socket(zmq.REQ)
    socket_pkda.connect("tcp://127.0.0.1:5555")  # Adjust the server IP address/port to that of PKDA server

    pu,pk = generate_keys()
    self_key_pair = {
        'public_key': f'{pu[0]},{pu[1]}',  
        'private_key': f'{pk[0]},{pk[1]}'
    }

    # save public key of self with PKDA
    save_public_key_of_self_with_pkda(initiator_id, self_key_pair["public_key"], socket_pkda)

    print()
    # Get the public key of client 2
    public_key_client2 = get_public_key_of_client_from_pkda(responder_id,socket_pkda)

    print("Public key of client 2", public_key_client2)
    print()

    # Exchange nonces to establish handshake
    socket_responder = context.socket(zmq.REQ)
    socket_responder.connect("tcp://127.0.0.1:5556")  # Adjust the server IP address/port to that of the responder
    # Send nonce to responder
    initiator_nonce = str(random.randint(0, 999999))
    message = f'{initiator_id}||{initiator_nonce}'
    print(f'Sending message containing "initiator_id||initiator_nonce": {message}')
    # Encrypt message with public key of responder
    message = encrypt(message, public_key_client2)
    socket_responder.send_string(message)
    response = socket_responder.recv_string()
    print(f'Encrypted response received: {response}')
    # Decrypt with private key of self
    response = decrypt(response, self_key_pair["private_key"])
    print(f'Decrypted response: {response}')
    responseElements = response.split('||')
    if len(responseElements) !=2 or responseElements[0]!=initiator_nonce:
        print('Nonce match failed at step 1')
    else:
        responder_nonce = responseElements[1]
    print()

    message = responder_nonce
    print(f'Sending message containing "responder_nonce":{message}')
    # Encrypt message with public key of responder
    message = encrypt(message, public_key_client2)
    print(f'Encrypted to: {message}')
    socket_responder.send_string(message)
    response = socket_responder.recv_string()
    print(f'Encrypted response received: {response}')
    # Decrypt with private key of self
    response = decrypt(response, self_key_pair["private_key"])
    print(f'Decrypted response: {response}')
    print()
    if response != 'OK':
        print('Nonce match failed at step 2')
    else:
        print('Nonces matched. Handshake complete')

    # Send the real messages to be exchanged
    for index in range(3):
        message = f'Hi{index+1}'
        print(f'Sending message {message}')
        # Encrypt message with public key of responder
        message = encrypt(message, public_key_client2)
        print(f'Encrypted to: {message}')
        socket_responder.send_string(message)
        response = socket_responder.recv_string()
        print(f'Encrypted response received: {response}')
        # Decrypt with private key of self
        response = decrypt(response, self_key_pair["private_key"])
        print(f'Decrypted response: {response}') 
        print()

def save_public_key_of_self_with_pkda(client_id, public_key_to_be_saved, socket_pkda):
    # Encrypt own public key using PKDA's public key
    encrypted_public_key = encrypt(public_key_to_be_saved,pkda_public_key)
    # share the public of the self to the PKDA
    message = f'Save {client_id} {encrypted_public_key}'
    while True:
        socket_pkda.send_string(message)
        response = socket_pkda.recv_string()
        # Decrypt the message using PKDA's public key
        decrypted_response = decrypt(response, pkda_public_key)
        if decrypted_response == 'OK':
            print(f'Saved public key with PKDA')
            break
        # If failed to save the public key, wait for 1 sec and try again
        print('Self public key could not be saved to PKDA.')
        time.sleep(1)
    return True

def get_public_key_of_client_from_pkda(client_id,socket_pkda):
    # Get the public key of client 2
    message = f'Get {client_id}||{time.time()}'
    print(f'Sending message {message}')
    while True:
        socket_pkda.send_string(message)
        response = socket_pkda.recv_string()
        # Decrypt the message using PKDA's public key
        decrypted_response = decrypt(response, pkda_public_key)
        public_key_client = decrypted_response.split('||')[0]
        if public_key_client != 'NOK':
            print(f'Encrypted response received: {response}')
            print(f'Decrypted response: {decrypted_response}')
            break
        # If the key is not available yet, wait for 1 sec and try again
        print(f'Waiting for {client_id} public key')
        time.sleep(1)
    return public_key_client

if __name__ == "__main__":
    initiator()
