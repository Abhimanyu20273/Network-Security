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

    # Encrypt own public key using PKDA's public key
    encrypted_public_key = encrypt(self_key_pair["public_key"],pkda_public_key)
    # share the public of the self to the PKDA
    message = f'Save {responder_id} {encrypted_public_key}'
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

    # Get the public key of client 2
    message = f'Get {initiator_id}||{time.time()}'
    while True:
        socket_pkda.send_string(message)
        response = socket_pkda.recv_string()
        print(f'Encrypted response: {response}')
        # Decrypt the message using PKDA's public key
        decrypted_response = decrypt(response, pkda_public_key)
        print(f'Decrypted response: {decrypted_response}')
        public_key_client1 = decrypted_response.split('||')[0]
        if public_key_client1 != 'NOK':
            break
        # If the key is not available yet, wait for 1 sec and try again
        print('Waiting for client1 public key')
        time.sleep(1)


    print("Public key of client 1", public_key_client1)

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

    responder_nonce = str(random.randint(0, 999990))
    return_message = f'{initiator_nonce}||{responder_nonce}'
    print(f'Sending response containing "initiator_nonce||responder_nonce": {return_message}')
    # Encrypt message with public key of initiator
    return_message = encrypt(return_message, public_key_client1)
    print(f'Encrypted to: {return_message}')
    socket2.send_string(return_message)
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


if __name__ == "__main__":
    responder()