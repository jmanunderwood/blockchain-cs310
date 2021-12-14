import hashlib
import json
from time import time

class Block(object):
    def __init__(self, index,nonce,previous_hash,data,timestamp=None):
        self.index=index
        self.nonce=nonce
        self.previous_hash=previous_hash
        self.data=data
        self.timestamp=timestamp or time()

    @property
    def hash(self): #calculate the block's hash
        block_string="{}{}{}{}{}".format(self.index,self.nonce,self.previous_hash,self.data,self.timestamp)
        block_encoded = block_string.encode()
        raw_hash = hashlib.sha256(block_encoded)
        hex_hash=raw_hash.hexdigest()
        return hex_hash

    @property
    def all_attributes(self):
        return dict(vars(self),hash=self.hash)

    def __str__(self):
        return json.dumps(self, sort_keys=True, default=lambda obj: obj.all_attributes) 

    
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    def genesis(self): #Create the Genesis block
        self.new_block(nonce=0,previous_hash=0)

    def new_block(self, nonce, previous_hash=None, data=None, timestamp=None): #Create a new block
        block=Block(
            index=len(self.chain),
            nonce=nonce,
            previous_hash=previous_hash,
            data=data or self.pending_transactions,
            timestamp=timestamp)
        self.pending_transactions=[]

        self.chain.append(block)
        return block

    def load_chain(self,chain):
        self.chain=chain

    def proof_of_work(self, previous):  #iterates through nonce values, returning the successful value
        new_nonce=1
        check=False

        while check==False:
            hash=hashlib.sha256(
                str(new_nonce**2-previous**2).encode()).hexdigest()
            if hash[:4]=="0000":    #require 4 leading digits of 0
                check=True
            else:
                new_nonce+=1
            
            print(str(new_nonce)+": "+hash[:4])
        return new_nonce
        
    def hash(self,block):
        block_string="{}{}{}{}{}".format(block.index,block.nonce,block.previous_hash,block.data,block.timestamp)
        block_encoded = block_string.encode()
        raw_hash = hashlib.sha256(block_encoded)
        hex_hash=raw_hash.hexdigest()

        return hex_hash

    def check_valid(self, chain): #check the validity of the chain
        previous=chain[0]
        index=1
        while index<len(chain):
            current=chain[index]
            
            if current.previous_hash != previous.hash:
                return False
        
            previous=current
            index+=1
        return True

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self,sender,recipient,amount): #Add a transaction to the current block
        self.pending_transactions.append({
            "sender":sender,
            "recipient":recipient,
            "amount":amount
        })
        return True

    def mine_block(self,miner_address): #mine the block
        self.new_transaction( 
            sender="0",
            recipient=miner_address,
            amount=1 #mining reward
        )
        previous_block=self.last_block
        nonce=self.proof_of_work(previous_block.nonce)

        previous_hash=previous_block.hash
        block=self.new_block(nonce,previous_hash=previous_hash)
