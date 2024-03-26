import socket             
from RSA_cryptosystem import encrypt, decrypt, generate_keys
 
s = socket.socket()         

port = 12345               
s.connect(('127.0.0.1', port)) 

pu_bytes = s.recv(1024)

pu_Authority = (int.from_bytes(pu_bytes[:256], 'big'), int.from_bytes(pu_bytes[256:], 'big'))

print("Received public key of authority: ",pu_Authority)

# s.close()