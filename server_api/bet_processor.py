import random

import eth_account.messages
from web3 import Web3
import os

# private key
key = os.getenv('PK')


def init_web3():
    return Web3(Web3.HTTPProvider('https://matic-mumbai.chainstacklabs.com'))


def check_tx(hash):
    w3 = init_web3()
    tx = w3.eth.get_transaction(hash)
    print(Web3.toInt(tx.value))

def simulate_game(amount,multiplier):
    payout = multiplier*amount
    cutoff = multiplier * (1/payout)
    random_number = random.randrange(0, multiplier*2)
    print(random_number,cutoff)
    if random_number<cutoff:
        return 'won'
    else:
        return 'busted'

def processBet(tx_hash, receiver, amount):
    w3 = init_web3()
    receiver = Web3.toChecksumAddress(receiver)
    messageHash = Web3.solidityKeccak(['address', 'uint256'], [receiver, amount])
    signableMessage = eth_account.messages.encode_defunct(messageHash)
    signedMessage = w3.eth.account.sign_message(signableMessage, key)
    responseDictionary = {'messageHash': Web3.toHex(signedMessage.messageHash),
                          'signature': to_32byte_hex(signedMessage.r) + to_32byte_hex(signedMessage.s).replace('0x',
                                                                                                               '') + Web3.toHex(
                              signedMessage.v).replace('0x', '')}
    return responseDictionary


def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


# check_tx('0xcd6d5f0157295cba3214485f32597b62842d138fd2b800a31921832161ed180e')
print(simulate_game(1,5))
