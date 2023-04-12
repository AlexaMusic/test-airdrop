from web3 import Web3
import os

w3 = Web3(Web3.HTTPProvider(os.environ['WEB3_PROVIDER']))

private_key = os.environ['PRIVATE_KEY']
account = w3.eth.account.privateKeyToAccount(private_key)

destination_address = os.environ['DESTINATION_ADDRESS']

def is_airdrop(tx_hash):
    tx = w3.eth.getTransaction(tx_hash)
    if tx.value > 0 and tx.to == account.address:
        return True
    else:
        return False

def transfer_airdrops():
    balance = w3.eth.getBalance(account.address)
    if balance > 0:
        tx = {
            'to': destination_address,
            'value': balance,
            'gas': 21000,
            'gasPrice': w3.toWei('20', 'gwei'),
            'nonce': w3.eth.getTransactionCount(account.address)
        }
        signed_tx = account.signTransaction(tx)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f'Transferred {balance} Wei to {destination_address} (Tx Hash: {tx_hash.hex()})')
        
print("Deployment successful!")
while True:
    try:
        latest_block = w3.eth.getBlock('latest')
        for tx_hash in latest_block['transactions']:
            if is_airdrop(tx_hash):
                transfer_airdrops()
        latest_block_hex = hex(latest_block.number)
        w3.eth.waitForTransactionReceipt(latest_block_hex, timeout=120)
    except:
        pass
