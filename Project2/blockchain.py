import json
import time
import random
import string

# Defines a single piece of the blockchain which are then stringed together
class Block:
# To make an object and initialize it
    def __init__(self, index, transactions_log, time_log, last_block_hash, nonce=0):
        self.index = index
        self.transactions_log = transactions_log
        self.time_log = time_log
        self.last_block_hash = last_block_hash
        self.nonce = nonce

# Computes hash to encode for the blockchain
    def Calculate_hash(self):
        return self.generate_random_string()

# Function used by Calculate_hash
    def generate_random_string(self, starts_with='00', stringLength=8):
        letters = string.ascii_lowercase
        hash = starts_with  + ''.join(random.choice(letters) for i in range(stringLength))
        print("Hash for the update" , hash)
        return hash


class Blockchain:
# Difficulty of our Proof of Work algorithm
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

# Bulids a genesis block and appends it to the chain. The block has index 0, last_block_hash as 0, and a valid hash.
    def create_genesis_block(self):
        genesis_block = Block(0, [], 0, "0")
        genesis_block.hash = genesis_block.Calculate_hash()
        self.chain.append(genesis_block)
        
# Using getters and settors to make code better
    @property
    def last_block(self):
        return self.chain[-1]

#  A function that adds the block to the chain after verification.
#        Verification includes:
#        * Checking if the proof is valid.
#        * The last_block_hash referred in the block and the hash of latest block
#          in the chain match.

    def add_block(self, block, proof):
        last_block_hash = self.last_block.hash

        if last_block_hash != block.last_block_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

# Try different values of nonce to get a hash
# that satisfies our difficulty criteria.
    @staticmethod
    def proof_of_work(block):
        block.nonce = 0
        computed_hash = block.Calculate_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.Calculate_hash()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def get_unconfirmed_transactions(self):
        return self.unconfirmed_transactions

# Check if block_hash is valid hash of block and satisfies
# the difficulty criteria.
    @classmethod
    def is_valid_proof(cls, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.Calculate_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        last_block_hash = "0"

        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `Calculate_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block_hash) or \
                    last_block_hash != block.last_block_hash:
                result = False
                break

            block.hash, last_block_hash = block_hash, block_hash
        return result
# It is an interface to add the pending
# transactions_log to the blockchain by adding them to the block
# and figuring out Proof Of Work.
    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions_log=self.unconfirmed_transactions,
                          time_log=time.time(),
                          last_block_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []

        return True


