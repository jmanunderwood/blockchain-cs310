import blockchain
from blockchain import Block
import hashlib
import json
from os.path import exists

address="Address"
data_path="data/"
blockchain=blockchain.Blockchain()

if not exists("data/block0.json"):
    blockchain.genesis()
    print("GENESIS")
    
i=0
while exists(data_path+"block"+str(i)+".json"):
    with open(data_path+"block"+str(i)+".json") as f:
        block=json.loads(f.read())
        blockchain.new_block(nonce=block["nonce"], previous_hash=block["previous_hash"], data=block["data"], timestamp=block["timestamp"])
    i+=1

cmd = ""
while cmd.lower() != "quit":
    cmd=input(">")
    if cmd.lower() == "send": #send coins
        to=input("Recipient: ")
        amount=input("Amount: ")
        blockchain.new_transaction(address,to, amount)

    if cmd.lower() == "mine": #mine block
        blockchain.mine_block(address)
        for i in range(len(blockchain.chain)):
            with open(data_path+"block"+str(i)+".json","w") as outfile:
                json.dump(blockchain.chain[i].all_attributes,outfile)

    if cmd.lower() == "out": #print out the entire chain
        for i in range(len(blockchain.chain)):
            print(json.dumps(blockchain.chain[i].all_attributes, indent=4))

    if cmd.lower() == "balance":
        bal=0
        for i in range(len(blockchain.chain)):
            for j in range(len(blockchain.chain[i].data)):
                if blockchain.chain[i].data[j]["recipient"]==address:
                    bal+=int(blockchain.chain[i].data[j]["amount"])
                elif blockchain.chain[i].data[j]["sender"]==address:
                    bal-=int(blockchain.chain[i].data[j]["amount"])
        print("Balance for "+address+" is: ")
        print(str(bal))

    if cmd.lower() == "valid":
        print(blockchain.check_valid(blockchain.chain))
