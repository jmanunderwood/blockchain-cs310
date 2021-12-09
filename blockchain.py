import hashlib
import json
from time import time

class Block(object):
    def __init__(self,index,nonce,previous_hash,data,timestamp=None):
        self.index=index
        self.nonce=nonce
        self.previous_hash=previous_hash
        self.data=data
        self.timestamp=timestamp or time()
        
    def hash(self):
        block_string="{}{}{}{}{}".format(self.index,self.nonce,self.previous_hash,self.data,self.timestamp)
        block_encoded = block_string.encode()
        raw_hash = hashlib.sha256(block_encoded)
        hex_hash=raw_hash.hexdigest()

        return hex_hash
    
    def __repr__(self):
        block={
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.data,
            'nonce': self.nonce,
            'previous_hash': self.previous_hash
        }
        return json.dumps(block, indent=4)

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.nodes=set()
        self.genesis() 

    def genesis(self):
        self.new_block(nonce=0,previous_hash=0)

    def new_block(self, nonce, previous_hash=None): #Create a new block
        block=Block(
            index=len(self.chain),
            nonce=nonce,
            previous_hash=previous_hash,
            data=self.pending_transactions)
        self.pending_transactions=[]

        self.chain.append(block)
        return block
        """
        block={
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        """

    def proof_of_work(self, previous):  #iterates through nonce values, returning the successful value
        new_nonce=1
        check=False

        while check==False:
            hash=hashlib.sha256(
                str(new_nonce**2-previous**2).encode()).hexdigest()
            if hash[:4]=='0000':    #require 5 leading digits of 0
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
            if current != self.hash(previous):
                return False
        
            previous=current
            index+=1
        return True

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self,sender,recipient,amount):
        self.pending_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount
        })
        return True

    def hash(self,block):
        block_encoded = json.dumps(block,sort_keys=True).encode()
        raw_hash = hashlib.sha256(block_encoded)
        hex_hash=raw_hash.hexdigest()

        return hex_hash

    def mine_block(self,miner_address):
        self.new_transaction( #mining reward
            sender="0",
            recipient=miner_address,
            amount=1
        )
        previous_block=self.last_block
        nonce=self.proof_of_work(previous_block.nonce)

        previous_hash=previous_block.hash()
        block=self.new_block(nonce,previous_hash)
        """
        previous_block=self.last_block
        nonce=self.proof_of_work(previous_block.nonce)
        previous_hash=self.hash(previous_block)
        self.new_block(nonce,previous_hash)
        """

    def create_node(self, address):
        self.nodes.add(address)
        return True