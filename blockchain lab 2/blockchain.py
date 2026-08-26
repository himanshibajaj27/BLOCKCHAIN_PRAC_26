import datetime
import hashlib
import json

from flask import Flask, jsonify


class Blockchain:

    def __init__(self):

        self.chain = []

        # Genesis Block
        self.create_block(
            proof=1,
            previous_hash='0'
        )

    # Create a block
    def create_block(self, proof, previous_hash):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }

        self.chain.append(block)

        return block

    # Get last block
    def get_previous_block(self):

        return self.chain[-1]

    # Proof of Work
    def proof_of_work(self, previous_proof):

        new_proof = 1

        while True:

            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()

            # Golden nonce condition
            if hash_operation[:3] == '000':
                return new_proof

            new_proof += 1

    # Hash a block
    def hash(self, block):

        encoded_block = json.dumps(
            block,
            sort_keys=True
        ).encode()

        return hashlib.sha256(encoded_block).hexdigest()

    # Check blockchain validity
    def is_chain_valid(self, chain):

        previous_block = chain[0]

        block_index = 1

        while block_index < len(chain):

            block = chain[block_index]

            # Check previous hash
            if block['previous_hash'] != self.hash(previous_block):
                return False

            # Check Proof of Work
            previous_proof = previous_block['proof']

            proof = block['proof']

            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()

            if hash_operation[:3] != '000':
                return False

            previous_block = block

            block_index += 1

        return True


# ------------------------------------------------------------
# Flask Application
# ------------------------------------------------------------

app = Flask(__name__)

blockchain = Blockchain()


# ------------------------------------------------------------
# Mine Block
# ------------------------------------------------------------

@app.route('/mine_block', methods=['GET'])
def mine_block():

    previous_block = blockchain.get_previous_block()

    previous_proof = previous_block['proof']

    # Find Golden Nonce
    proof = blockchain.proof_of_work(previous_proof)

    # Get previous block hash
    previous_hash = blockchain.hash(previous_block)

    # Create new block
    block = blockchain.create_block(
        proof,
        previous_hash
    )

    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    return jsonify(response), 200


# ------------------------------------------------------------
# Get Blockchain
# ------------------------------------------------------------

@app.route('/get_chain', methods=['GET'])
def get_chain():

    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200


# ------------------------------------------------------------
# Check Validity
# ------------------------------------------------------------

@app.route('/is_valid', methods=['GET'])
def is_valid():

    valid = blockchain.is_chain_valid(
        blockchain.chain
    )

    if valid:

        response = {
            'message': 'All good. The Blockchain is valid.'
        }

    else:

        response = {
            'message': 'Houston, we have a problem. The Blockchain is not valid.'
        }

    return jsonify(response), 200


# ------------------------------------------------------------
# Run Server
# ------------------------------------------------------------

if __name__ == '__main__':

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )