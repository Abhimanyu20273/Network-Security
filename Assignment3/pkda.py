import zmq
from RSA_cryptosystem import generate_keys, encrypt, decrypt

PKDA_key_pair = {
    'public_key': '5501485559,3109',
    'private_key': '5501485559,1550071213'
}

client_public_keys = {}

def pkda():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")  # Adjust the port as needed
    print("PKDA Server is running...")

    while True:
        # Wait for a request from a client
        message = socket.recv_string()
        print(f'Received {message}')
        # Note: The message to PKDA is not encrypted, only the client's key when sent in a 'Save' request is encrypted
        messageElts = message.split(' ')
        return_message = 'NOK'
        if messageElts[0] == 'Save':
            # This is a save request. Save to client_public_keys
            # Format: Save <client_id> <encrypted_public_key>
            if len(messageElts) == 3:
                client_id = messageElts[1]
                encrypted_public_key = messageElts[2]
                # Decrypt the encrypted public key using PKDA's private key
                public_key = decrypt(encrypted_public_key,PKDA_key_pair['private_key'])
                print(f'{client_id} decrypted public key: {public_key}')
                client_public_keys[client_id] = public_key
                return_message = 'OK'
                print(f'All the saved public keys after Save operation are: {client_public_keys}')
        elif messageElts[0] == 'Get':
            # Format: Get <client_id>||<time>
            if len(messageElts) == 2:
                # This is a get request. Return value from client_public_keys
                timestamp = messageElts[1].split('||')[1]
                client_id = messageElts[1].split('||')[0]
                # Encrypt the client's public key using PKDA's private key
                return_message = f"{client_public_keys.get(client_id,'NOK')}||{timestamp}"
        # Encrypt message with POKDA private key
        print(f'Sending response {return_message}')
        return_message = encrypt(return_message, PKDA_key_pair['private_key'])
        print(f'Encrypted to: {return_message}')
        print()
        socket.send_string(return_message)

if __name__ == "__main__":
    pkda()