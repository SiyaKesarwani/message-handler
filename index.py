import asyncio
import random
import time
from queue import Queue
from threading import Thread
from web3 import Web3
import os
import dotenv

dotenv.load_dotenv()  # loads .env file from current directory

# Define the words for message generation
WORDS = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]

# Ethereum settings (make sure to replace these with your actual addresses and token details)
RPC_NODE_URL = os.getenv('RPC_NODE_URL')
TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS')
SOURCE_ADDRESS = os.getenv('SOURCE_ADDRESS')
TARGET_ADDRESS = os.getenv('TARGET_ADDRESS')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

TYPES_ACCEPTED = ['hello', 'crypto']

# ERC-20 Token ABI
ERC20_ABI = '''
[
    {"constant": true, "inputs": [{"name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "payable": false, "stateMutability": "view", "type": "function"},
    {"constant": false, "inputs": [{"name": "to", "type": "address"}, {"name": "value", "type": "uint256"}], "name": "transfer", "outputs": [{"name": "", "type": "bool"}], "payable": false, "stateMutability": "nonpayable", "type": "function"},
    {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}
]
'''

# Parent Agent class
class Agent:
    def __init__(self, inbox, outbox):
        self.inbox = inbox
        self.outbox = outbox
        self.handlers = {}

    # Parent has info of all handlers
    def register_handler(self, message_type, handler):
        self.handlers[message_type] = handler

    # Setting Outbox message
    def emit_message(self, message):
        self.outbox.put(message)

    # Process Inbox message
    def process_inbox(self):
        while True:
            message = self.inbox.get()
            if message is None:  # Shutdown signal
                break
            message_type = message.get('type')
            if message_type in self.handlers:
                self.handlers[message_type](message)
