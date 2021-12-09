import blockchain
import json

blockchain=blockchain.Blockchain()
cmd = ""
while cmd.lower() != "quit":
    cmd=input(">")
    if cmd.lower() == "add": #add transaction
        sender=input("From: ")
        recipient=input("To: ")
        amount=input("How much: ")
        blockchain.new_transaction(sender,recipient,amount)

    if cmd.lower() == "mine": #mine block
        blockchain.mine_block()

    if cmd.lower() == "out":
        print("Chain: ",blockchain.chain)

    if cmd.lower() == "exp":
        with open('chain.txt','w') as outfile:
            json.dump(blockchain.chain, outfile)
        print("Chain: ",blockchain.chain)

    if cmd.lower() == "imp":
        with open('chain.txt') as json_file:
            blockchain.chain=json.load(json_file)
        print("Chain: ",blockchain.chain)

    if cmd.lower() == "bal":
        account=input("Account: ")

    if cmd.lower() == "gettx":
        account=input("Account: ")
        transaction=input("TxID: ")

    if cmd.lower() == "listtx":
        account=input("Account: ")

    if cmd.lower() == "valid":
        print(blockchain.check_valid())

print("Chain: ",blockchain.chain)

