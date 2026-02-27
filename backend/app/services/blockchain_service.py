import json
from web3 import Web3
from app.core.config import settings

w3 = Web3(Web3.HTTPProvider(settings.GANACHE_URL))

ABI = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"_candidateId","type":"uint256"}],"name":"votedEvent","type":"event"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"candidatesCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_candidateId","type":"uint256"}],"name":"vote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]')


def _get_contract():
    if not settings.CONTRACT_ADDRESS:
        return None
    return w3.eth.contract(address=settings.CONTRACT_ADDRESS, abi=ABI)


class BlockchainService:
    @staticmethod
    def is_connected():
        return w3.is_connected()

    @staticmethod
    def get_free_wallet(users_count: int) -> str:
        accounts = w3.eth.accounts
        index = users_count + 1
        if index >= len(accounts):
            raise ValueError("Ganache'da bosh hamyon yoq!")
        return accounts[index]

    @staticmethod
    def vote_in_blockchain(candidate_id: int, voter_address: str) -> bool:
        contract = _get_contract()
        if not contract:
            print("OGOHLANTIRISH: CONTRACT_ADDRESS yoq.")
            return True
        try:
            tx_hash = contract.functions.vote(candidate_id).transact({"from": voter_address})
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt.status == 1
        except Exception as e:
            print(f"Blokcheyn xatosi: {e}")
            return False

    @staticmethod
    def get_candidate_votes(candidate_id: int) -> int:
        contract = _get_contract()
        if not contract:
            return 0
        try:
            candidate = contract.functions.candidates(candidate_id).call()
            return candidate[2]
        except Exception:
            return 0
