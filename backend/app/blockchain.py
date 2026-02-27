import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

GANACHE_URL = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

# Kontrakt ma'lumotlari
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# ABI-ni matn ko'rinishida json.loads ichiga joylashtiramiz
ABI = json.loads('''
[
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": true,
                "internalType": "uint256",
                "name": "_candidateId",
                "type": "uint256"
            }
        ],
        "name": "votedEvent",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "candidates",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "id",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "name",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "voteCount",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "candidatesCount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_candidateId",
                "type": "uint256"
            }
        ],
        "name": "vote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "name": "voters",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
''')

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def vote_in_blockchain(candidate_id, voter_address):
    """Blokcheynda ovoz berish tranzaksiyasini amalga oshiradi"""
    try:
        tx_hash = contract.functions.vote(candidate_id).transact({'from': voter_address})
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return receipt.status == 1
    except Exception as e:
        print(f"Blokcheyn xatosi: {e}")
        return False

def get_candidate_votes_from_bc(candidate_id):
    """Nomzodning ovozlar sonini blokcheyndan o'qiydi"""
    try:
        candidate = contract.functions.candidates(candidate_id).call()
        return candidate[2] # voteCount
    except:
        return 0