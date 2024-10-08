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

# Child Agent class
class ConcreteAgent(Agent):
    
    # Constructor with its Inbox and Outbox
    def __init__(self, inbox, outbox):
        super().__init__(inbox, outbox)
        self.w3 = Web3(Web3.HTTPProvider(RPC_NODE_URL))
        self.token_contract = self.w3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=ERC20_ABI)
        self.register_handler('hello', self.handle_hello)
        self.register_handler('crypto', self.handle_crypto)

    # "hello" keyword handler
    def handle_hello(self, message_content):
            print(f"Filtered message (hello): {message_content['content']}")

    # "crypto" keyword & transfer ERC20 handler
    def handle_crypto(self, message_content):
            self.transfer_token()

    # "random message generator" behaviour
    async def generate_random_message(self):
        while True:
            message_content = f"{random.choice(WORDS)} {random.choice(WORDS)}"
            type = "message"
            for i in range (len(TYPES_ACCEPTED)):
                if TYPES_ACCEPTED[i] in message_content:
                    type = TYPES_ACCEPTED[i]
                    break
            self.emit_message({'type': type, 'content': message_content})
            await asyncio.sleep(2) #Generates random 2-word messages every 2 seconds.

    # "ERC20 balance checker" behaviour
    async def check_balance(self):
        while True:
            balance = self.token_contract.functions.balanceOf(self.w3.to_checksum_address(SOURCE_ADDRESS)).call()
            print(f"ERC-20 Token Balance: {self.w3.from_wei(balance, 'ether')} tokens")
            await asyncio.sleep(10) #Checks the ERC-20 token balance of an ethereum address every 10 seconds

    # transfer token based on current balance
    def transfer_token(self):
        balance = self.token_contract.functions.balanceOf(self.w3.to_checksum_address(SOURCE_ADDRESS)).call()
        one_unit = 1*10**(self.token_contract.functions.decimals().call())
        if balance >= one_unit:
            nonce = self.w3.eth.get_transaction_count(SOURCE_ADDRESS)
            tx = self.token_contract.functions.transfer(TARGET_ADDRESS, one_unit).build_transaction({
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price, 
                'chainId': self.w3.eth.chain_id
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            _ = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f"Token transfer sent! Transaction hash: {self.w3.to_hex(tx_hash)}")
        else:
            print("Not enough tokens to transfer.")

    # starts running behaviours continuously
    def start(self):
        # Start behavior tasks
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.generate_random_message())
        loop.create_task(self.check_balance())
        loop.run_forever()
def setUpTask():
    # Create message queues
    inbox1 = Queue()
    outbox1 = Queue()
    inbox2 = Queue()
    outbox2 = Queue()

    # Instantiate agents
    agent1 = ConcreteAgent(inbox1, outbox1)
    agent2 = ConcreteAgent(inbox2, outbox2)

    # Start processing messages in threads
    Thread(target=agent1.process_inbox, daemon=True).start()
    Thread(target=agent2.process_inbox, daemon=True).start()

    # Start the agents' behaviors
    Thread(target=agent1.start, daemon=True).start()
    Thread(target=agent2.start, daemon=True).start()

    # Connect the agents' inboxes and outboxes
    while True:
        # Relay messages between agents
        if not outbox1.empty():
            message = outbox1.get()
            inbox2.put(message)

        if not outbox2.empty():
            message = outbox2.get()
            inbox1.put(message)

        time.sleep(1)

if __name__ == '__main__':
    setUpTask()