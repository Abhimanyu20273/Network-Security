from flask import Flask, jsonify, request
from flask_cors import CORS

from RSA_cryptosystem import generate_keys, encrypt, decrypt

app = Flask(__name__)
CORS(app)
app.secret_key = 'pkda_app_key'

PKDA_key_pair = {
    'public_key': '5501485559,3109',
    'private_key': '5501485559,1550071213'
}

public_keys = {
    'registrar': '5282963831,1343',
    'director': '5060330447,3149'
}


@app.route('/get_public_key', methods=['GET'])
def get_public_key():
    client_id = request.args.get('client_id',None)
    client_public_key = public_keys.get(client_id,'')
    if client_public_key:
        # Encrypt message with PKDA private key
        retDict = {
            'encrypted_public_key': encrypt(client_public_key, PKDA_key_pair['private_key'])
        }
        print(f'Returning: {retDict}')
        return jsonify(retDict), 200
    else:
        return jsonify({}), 404

if __name__ == "__main__":
    app.run(debug=True, port = 5002)