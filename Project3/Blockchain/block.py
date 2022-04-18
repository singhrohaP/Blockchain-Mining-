import time
from hashlib import sha256

# class to create blocks using sha256 hash
class Block(object):

    def __init__( self, index=0, nonce=0, previous_hash=None, data=None, hash=None, timestamp=None ):
        self.index = index
        self.previous_hash = previous_hash or '0'
        self.timestamp = timestamp or time.time()
        self.data = data or ''
        self.nonce = nonce
        self.hash = hash or self.calculateHash()

    def to_dict(self):
        return {
            'index': self.index,
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'data': self.data,
            'nonce': self.nonce,
            'hash': self.hash
        }

    @staticmethod

    # function to create genesis block
    def genesis():
        genesisBlock = Block( 0, 0, '0', 'Genesis Block', [], 1520572079.336289)
        genesisBlock.hash = genesisBlock.calculateHash()
        return genesisBlock

    # function to calculate hash
    def calculateHash(self):
        original_str = ''.join([
            str(self.index), self.previous_hash, str(self.timestamp), self.data,
            str(self.nonce)])
        return sha256(original_str.encode('utf-8')).hexdigest()

    # function to verifies new block by comparing the hash value from previous block
    def __eq__(self, other):
        if ( self.index == other.index and 
             self.previous_hash == other.previous_hash and 
             self.timestamp == other.timestamp and 
             self.data == other.data and 
             self.nonce == other.nonce and
             self.hash == other.hash ):
            return True
        return False
