import json
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from web3 import Web3
from web3.middleware import geth_poa_middleware

# private key
# account 1 key
key = "0xe8d71d1e4c1c28754ad7c5938ac301c2a6512cc69b0b10bd1c9864a5bb6c1c9f"
# rpc provider
provider = "https://data-seed-prebsc-1-s1.binance.org:8545/"
# provider = "https://bsc-dataseed.binance.org/"
# token address
tokenAddress = "0x5529a8C432362D751eA829704ec6fAf6c478Bdbd"
# chain ID
chain_id = 97


def Connect():
    return Web3(Web3.HTTPProvider(provider))


def is_Connected(conn):
    return conn.isConnected()


def getNonce(conn):
    return conn.eth.get_transaction_count(conn.eth.account.privateKeyToAccount(key).address)


def getNFTAbi():
    return json.load(open(os.path.join(os.path.dirname(__file__), 'nftabi.json'), 'r'))


def getNFTContract(conn):
    return conn.eth.contract(address=Web3.toChecksumAddress(tokenAddress), abi=getNFTAbi())


def mintReward(address):
    conn = Connect()
    # zaroori
    conn.middleware_onion.inject(geth_poa_middleware, layer=0)
    NFTContract = getNFTContract(conn)
    options = {
        'chainId': 0x61,
        'from': conn.eth.account.privateKeyToAccount(key).address,
        'nonce': getNonce(conn),
        'gasPrice': conn.eth.gas_price,
    }
    tx = NFTContract.functions.mintReward(3, Web3.toChecksumAddress(address)).build_transaction(options)
    signedTx = conn.eth.account.sign_transaction(tx, key)
    txHash = conn.eth.send_raw_transaction(signedTx.rawTransaction)
    result = conn.eth.wait_for_transaction_receipt(txHash)
    return HttpResponse(result['status'])
