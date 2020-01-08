import hashlib
import requests
import json
import sys
from uuid import uuid4
from timeit import default_timer as timer
import random
import time
def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_proof: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """
    proof = 1000000
    while valid_proof(last_proof, proof) is False:
        proof += 1
    print("Proof found: " + str(proof))
    return proof
def valid_proof(last_proof, proof):
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?
    IE:  last_proof: ...AE9123456, new hash 123456E88...
    """
if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"
    coins_mined = 0
    # Load or create ID
    # Run forever until interrupted
    while True:
        headers = { "content-type": "application/json",
                    "Authorization": f'Token 83836d69849450074fcc3292ee2d6a3975d46574'}
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof", headers=headers)
        data = r.json()
        last_proof = data.get('proof')
        new_proof = proof_of_work(last_proof)
        post_data = {"proof": new_proof}
        r = requests.post(url=node + "/mine", json=post_data, headers=headers)
        data = r.json()
        print(data)
        time.sleep(10)
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))