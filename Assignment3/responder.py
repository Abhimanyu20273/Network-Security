import zmq
import time
import random
from RSA_cryptosystem import generate_keys, encrypt, decrypt

pkda_id = 'pkda_id'
initiator_id = 'client_1'
responder_id = 'client_2'

pkda_public_key = '5501485559,3109'


def responder():
    # Create a ZeroMQ connection to send requests and get responses from the PKDA server
    context = zmq.Context()
    socket_pkda = context.socket(zmq.REQ)
    socket_pkda.connect("tcp://127.0.0.1:5555")  # Adjust the server IP address/port to that of PKDA server

    pu,pk = generate_keys()
    self_key_pair = {
        'public_key': f'{pu[0]},{pu[1]}',  
        'private_key': f'{pk[0]},{pk[1]}'
    }

    public_key_client1 = None

    # save public key of self with PKDA
    save_public_key_of_self_with_pkda(responder_id, self_key_pair["public_key"], socket_pkda)

    print()
    socket2 = context.socket(zmq.REP)
    socket2.bind("tcp://*:5556")  # Adjust the port as needed
    print("Responder ready to receive messages...")

    # Exchange nonces to establish handshake
    # Wait for a request from initiator
    message = socket2.recv_string()
    print(f'Received {message}')
    # Decrypt message with own private key
    message = decrypt(message, self_key_pair['private_key'])
    print(f'Decrypted message: {message}')
    responseElements = message.split('||')
    if len(responseElements) !=2 or responseElements[0] != initiator_id:
        print('Nonce match failed at step 1')
    else:
        initiator_nonce = responseElements[1]

    # Get the public key of the initiator for encrypting messages to it
    public_key_client1 = get_public_key_of_client_from_pkda(initiator_id,socket_pkda)
    print("Public key of client 1", public_key_client1)

    responder_nonce = str(random.randint(0, 999990))
    return_message = f'{initiator_nonce}||{responder_nonce}'
    print(f'Sending response containing "initiator_nonce||responder_nonce": {return_message}')
    # Encrypt message with public key of initiator
    return_message = encrypt(return_message, public_key_client1)
    print(f'Encrypted to: {return_message}')
    socket2.send_string(return_message)
    print()
    # Wait for a response from initiator
    message = socket2.recv_string()
    print(f'Received {message}')
    # Decrypt message with own private key
    message = decrypt(message, self_key_pair['private_key'])
    print(f'Decrypted to: {message}')
    if responder_nonce == message:
        return_message = 'OK'
        # Encrypt message with public key of initiator
        print(f'Sending response {return_message}')
        return_message = encrypt(return_message, public_key_client1)
        print(f'Encrypted to: {return_message}')
        socket2.send_string(return_message)
        print('Nonces matched. Handshake complete')
    else:
        print('Nonce match failed')
    print()

    # Listen for the real messages to be received
    while True:
        # Wait for a request from initiator
        message = socket2.recv_string()
        print(f'Received {message}')
        # Decrypt message with own private key
        message = decrypt(message, self_key_pair['private_key'])
        print(f'Decrypted to: {message}')
        if message[:2] == 'Hi':
            index = message[2]
        return_message = f'Got-it{index}'
        print(f'Sending response {return_message}')
        # Encrypt message with public key of initiator
        return_message = encrypt(return_message, public_key_client1)
        print(f'Encrypted to: {return_message}')
        socket2.send_string(return_message)

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
    responder()