import json
import random
import string

import eth_account.messages
from web3 import Web3
import os

# private key
key = os.getenv('PK')

rewarder_contract_address = Web3.to_checksum_address('0x878dcf237992bbe92421e00291d928097af759b3')
contract_creation_block = Web3.to_hex(37815830)

with open('rewarder_abi.json') as file:
    rewarder_abi = json.load(file)


def init_web3():
    # to-do: add code for multichain
    return Web3(Web3.HTTPProvider('https://polygon-mumbai.g.alchemy.com/v2/aOTeKN6mSI-1aHNoAVX3VNAUa3QJ6Kja'))


def verify_transaction_hash(tx_hash, value):
    w3 = init_web3()
    tx = w3.eth.get_transaction(tx_hash)
    tx_value = Web3.to_int(tx.value)
    print(tx_value)
    if value != tx_value:
        return False
    else:
        tx_hash_reuse_check(tx_hash)


def get_contract():
    return init_web3().eth.contract(address=rewarder_contract_address, abi=rewarder_abi)


def tx_hash_reuse_check(tx_hash):
    contract = get_contract()
    print(contract.address)
    event_filter = contract.events.claimSuccess.create_filter(fromBlock=contract_creation_block,
                                                              argument_filters={'tx': tx_hash})
    event = event_filter.get_all_entries()
    if len(event) == 0:
        return True
    return False


def get_cutoff(amount, multiplier):
    k = random.randint(1, 100)
    rand = ''.join(random.choices(string.ascii_uppercase, k=k))
    hashed = hash(rand)
    cutoff = random.randrange(80, 2000) / (hashed * (amount * multiplier) * 0.2)
    cutoff = str(cutoff).split('.')
    cutoff = float(cutoff[0] + '.' + cutoff[1][1:3])
    cutoff = max([1, cutoff])
    print(cutoff)
    return cutoff


def processBet(receiver, amount, multiplier, tx_hash):
    w3 = init_web3()
    if tx_hash_reuse_check(tx_hash):
        cutoff = get_cutoff(amount, multiplier)
        if cutoff > multiplier:
            receiver = Web3.to_checksum_address(receiver)
            messageHash = Web3.solidity_keccak(['address', 'uint256', 'string'], [receiver, int(amount), tx_hash])
            signableMessage = eth_account.messages.encode_defunct(messageHash)
            signedMessage = w3.eth.account.sign_message(signableMessage, key)
            responseDictionary = {'messageHash': Web3.to_hex(signedMessage.messageHash),
                                  'signature': to_32byte_hex(signedMessage.r) + to_32byte_hex(signedMessage.s).replace(
                                      '0x',
                                      '') + Web3.to_hex(
                                      signedMessage.v).replace('0x', ''), 'response': 'won', 'cutoff': cutoff}
            return responseDictionary
        else:
            return {'response': 'busted'}
    else:
        return {'response': 'Invalid tx_hash'}


def to_32byte_hex(val):
    return Web3.to_hex(Web3.to_bytes(val).rjust(32, b'\0'))
