import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash="Genesis",nonce=100) #Genesis block
    
    def new_block(self, nonce, previous_hash=None): #Create a new block
        block={
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.pending_transactions=[]
        self.chain.append(block)

        return block

    def proof_of_work(self, previous):  #iterates through nonce values, returning the successful value
        new_nonce=1
        check=False

        while check==False:
            hash=hashlib.sha256(
                str(new_nonce**2-previous**2).encode()).hexdigest()
            if hash[:5]=='00000':    #require 5 leading digits of 0
                check=True
            else:
                new_nonce+=1
            
            print(str(new_nonce)+": "+hash[:4])
        return new_nonce

    def check_valid(self, chain):
        previous=chain[0]
        index=1
        while index<len(chain):
            current=chain[index]
            if current['previous_hash'] != self.hash(previous):
                return False
        
            previous=current
            index+=1
        return True

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self,sender,recipient,amount):
        transaction={
            'sender':sender,
            'recipient':recipient,
            'amount':amount
        }
        self.pending_transactions.append(transaction)
        return self.last_block['index']+1

    def hash(self,block):
        block_encoded = json.dumps(block,sort_keys=True).encode()
        raw_hash = hashlib.sha256(block_encoded)
        hex_hash=raw_hash.hexdigest()

        return hex_hash

    def mine_block(self):
        previous_block=self.last_block
        nonce=self.proof_of_work(previous_block["nonce"])
        previous_hash=self.hash(previous_block)
        self.new_block(nonce,previous_hash)
        
