import json
import os

import eth_account.messages
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.auto import w3

# private key
# account key
key = "0xe8d71d1e4c1c28754ad7c5938ac301c2a6512cc69b0b10bd1c9864a5bb6c1c9f"
# # rpc provider
# provider = "https://mainnet.infura.io/v3/e8d3fa6932da49eba3051b007152a8bb"
# token address
tokenAddress = "0xbA3E5F8b4200a5eb856FF2C3E001aB29444491AA"
# # chain ID
# chain_id = 97
# # token decimals
# decimals = 18
#
#
# def Connect():
#     return Web3(Web3.HTTPProvider(provider))
#
#
# def is_Connected(conn):
#     return conn.isConnected()
#
#
# def getNonce(conn):
#     return conn.eth.get_transaction_count(conn.eth.account.privateKeyToAccount(key).address)
#
#
# def getAbi():
#     return json.load(open(os.path.join(os.path.dirname(__file__), 'abi.json'), 'r'))
#
#
# def getTokenContract(conn):
#     return conn.eth.contract(address=Web3.toChecksumAddress(tokenAddress), abi=getAbi())
#
#
# def transferReward(address, amount):
#     conn = Connect()
#     # zaroori
#     conn.middleware_onion.inject(geth_poa_middleware, layer=0)
#     contract = getTokenContract(conn)
#     options = {
#         'chainId': 0x1,
#         'from': conn.eth.account.privateKeyToAccount(key).address,
#         'nonce': getNonce(conn),
#         'gasPrice': conn.eth.gas_price,
#     }
#     burnAmount, transferAmount = getAmounts(int(amount.split('.')[0]))
#     tx = contract.functions.transfer(Web3.toChecksumAddress(address), int(transferAmount)).build_transaction(options)
#     signedTx = conn.eth.account.sign_transaction(tx, key)
#     txHash = conn.eth.send_raw_transaction(signedTx.rawTransaction)
#     result = conn.eth.wait_for_transaction_receipt(txHash)
#     if result['status'] == 1:
#         burn(burnAmount, conn)
#     return result['status']
#
#
# def burn(burnAmount, conn):
#     contract = getTokenContract(conn)
#     options = {
#         'chainId': 0x1,
#         'from': conn.eth.account.privateKeyToAccount(key).address,
#         'nonce': getNonce(conn),
#         'gasPrice': conn.eth.gas_price,
#     }
#     tx = contract.functions.burn(burnAmount).build_transaction(options)
#     signedTx = conn.eth.account.sign_transaction(tx, key)
#     txHash = conn.eth.send_raw_transaction(signedTx.rawTransaction)
#     result = conn.eth.wait_for_transaction_receipt(txHash)
#     if result['status'] == 1:
#         print("Burned successfull!")
#     else:
#         print("Burned Failed!")
#
#
# def getAmounts(amount):
#     burnAmount = int(amount * (10 / 100))
#     return burnAmount * (10 ** decimals), (amount - burnAmount) * (10 ** decimals)


def signClaimToken(receiver,amount):
    messageHash = Web3.solidityKeccak(['address', 'uint256'], [receiver, amount])
    signableMessage = eth_account.messages.encode_defunct(messageHash)
    signedMessage = w3.eth.account.sign_message(signableMessage, key)
    responseDictionary = {'messageHash': Web3.toHex(signedMessage.messageHash), 'signature': to_32byte_hex(signedMessage.r) + to_32byte_hex(signedMessage.s).replace('0x','') + Web3.toHex(signedMessage.v).replace('0x','')}
    return responseDictionary


def to_32byte_hex(val):
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))
