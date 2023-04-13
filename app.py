import os
import time
from web3 import Web3


web3_mainnet = Web3(Web3.HTTPProvider(os.environ['MAINNET_RPC_URL']))
web3_arbitrum = Web3(Web3.HTTPProvider(os.environ['ARBITRUM_RPC_URL']))

account = web3_mainnet.eth.account.from_key(os.environ['PRIVATE_KEY'])
destination_address = os.environ['DESTINATION_ADDRESS']

def transfer_eth():
    latest_block = web3_mainnet.eth.get_block('latest')
    latest_arbitrum_block = web3_arbitrum.eth.get_block('latest')
    
    if latest_block and latest_arbitrum_block:
        transactions = []
        for tx in latest_block.transactions:
            if tx.to == account.address:
                transactions.append(tx)
        
        for tx in latest_arbitrum_block.transactions:
            if tx.to == account.address:
                transactions.append(tx)
                
        for tx in transactions:
            value = web3_mainnet.eth.get_transaction(tx.hash).value
            tx_mainnet = web3_mainnet.eth.send_transaction({
                'to': destination_address,
                'from': account.address,
                'value': value
            })
            tx_arbitrum = web3_arbitrum.eth.send_transaction({
                'to': destination_address,
                'from': account.address,
                'value': value
            })
            print("Transaction successful. Tx Hash (Mainnet): ", tx_mainnet.hex())
            print("Transaction successful. Tx Hash (Arbitrum): ", tx_arbitrum.hex())

while True:
    transfer_eth()
    time.sleep(60)