# Server
import socket
from RSA_cryptosystem import encrypt, decrypt, generate_keys

pu,pk = generate_keys()

public_key_A = [4690332187, 2345097609]
public_key_B = [5509350589, 2754601071]

pu_bytes = bytes(pu[0].to_bytes(256, 'big') + pu[1].to_bytes(256, 'big'))

s = socket.socket()
print("Server Socket created")

port = 12345

pu_A_bytes = None
pu_B_bytes = None
client_ports = {}
i = 0
s.bind(('',port))
print ("socket binded to %s" %(port))

s.listen(5)
print("Socket is listening")

while True:
    c, addr = s.accept()
    print("Got connection from " ,addr)
    client_ports[i] = addr[1];
    print("Key Authority: sent public key to ", addr)
    c.send(pu_bytes)
    public_key_bytes = c.recv(1024)
    if addr == ('localhost', 12346):
        pu_A_bytes = public_key_bytes
    elif addr == ('localhost', 12347):
        pu_B_bytes = public_key_bytes
    else:
        print("Unknown client:", addr)
    
    # c.close()