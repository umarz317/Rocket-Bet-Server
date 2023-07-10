import eth_account.messages
from web3 import Web3
from web3.auto import w3

# private key
key = "0xe8d71d1e4c1c28754ad7c5938ac301c2a6512cc69b0b10bd1c9864a5bb6c1c9f"


def signClaimToken(receiver,amount):
    receiver = Web3.toChecksumAddress(receiver)
    messageHash = Web3.solidityKeccak(['address', 'uint256'], [receiver, amount])
    signableMessage = eth_account.messages.encode_defunct(messageHash)
    signedMessage = w3.eth.account.sign_message(signableMessage, key)
    responseDictionary = {'messageHash': Web3.toHex(signedMessage.messageHash), 'signature': to_32byte_hex(signedMessage.r) + to_32byte_hex(signedMessage.s).replace('0x','') + Web3.toHex(signedMessage.v).replace('0x','')}
    return responseDictionary


def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))
