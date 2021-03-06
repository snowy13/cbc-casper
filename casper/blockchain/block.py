"""The block module implements the message data structure for a blockchain"""
from casper.message import Message


class Block(Message):
    """Message data structure for blockchain consensus"""

    def __init__(self, estimate, justification, sender):
        # Do some type checking for safety!
        assert isinstance(estimate, Block) or estimate is None, "...expected a prevblock!"

        super().__init__(estimate, justification, sender)

        # height is the traditional block height - number of blocks back to genesis block
        if estimate:
            self.height = estimate.height + 1
        else:
            self.height = 1

    def conflicts_with(self, message):
        """Returns true if self is not in the prev blocks of other_message"""
        assert isinstance(message, Block), "...expected a block"

        return not self.is_in_blockchain(message)

    def is_in_blockchain(self, block):
        """Returns True if self is an ancestor of block."""
        assert isinstance(block, Block), "...expected a block"

        if self == block:
            return True

        if block.estimate is None:
            return False

        return self.is_in_blockchain(block.estimate)
