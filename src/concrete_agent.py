import dotenv
dotenv.load_dotenv()  # loads .env file from current directory
import asyncio
import random
from utils.abi import ERC20_ABI
from utils.constants import WORDS, TYPES_ACCEPTED
from functionalities.autonomous_agent import Agent
from web3 import Web3
import os

# Ethereum settings (make sure to replace these with your actual addresses and token details)
RPC_NODE_URL = os.getenv('RPC_NODE_URL')
TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS')
SOURCE_ADDRESS = os.getenv('SOURCE_ADDRESS')
TARGET_ADDRESS = os.getenv('TARGET_ADDRESS')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')

class ConcreteAgent(Agent):
    '''
    This is Child Agent class which is responsible for 
    processing processing agent behaviours and also 
    send messages to Outbox.
    '''
    def __init__(self, inbox, outbox):
        ''' Constructor with its Inbox and Outbox '''
        super().__init__(inbox, outbox) # calling the constructor of base class
        self.w3 = Web3(Web3.HTTPProvider(RPC_NODE_URL))
        self.token_contract = self.w3.eth.contract(address=Web3.to_checksum_address(TOKEN_ADDRESS), abi=ERC20_ABI)
        self.register_handler('hello', self.handle_hello)
        self.register_handler('crypto', self.handle_crypto)

    def handle_hello(self, message_content):
        ''' "hello" keyword handler '''
        print(f"Filtered message (hello): {message_content['content']}")

    def handle_crypto(self, message_content):
        ''' "crypto" keyword & transfer ERC20 handler'''
        self.transfer_token()

    async def generate_random_message(self):
        ''' "random message generator" behaviour'''
        while True:
            message_content = f"{random.choice(WORDS)} {random.choice(WORDS)}"
            type = "message"
            for i in range (len(TYPES_ACCEPTED)):
                if TYPES_ACCEPTED[i] in message_content:
                    type = TYPES_ACCEPTED[i]
                    break
            self.emit_message({'type': type, 'content': message_content})
            await asyncio.sleep(2) #Generates random 2-word messages every 2 seconds.

    async def check_balance(self):
        ''' "ERC20 balance checker" behaviour'''
        while True:
            balance = self.token_contract.functions.balanceOf(self.w3.to_checksum_address(SOURCE_ADDRESS)).call()
            print(f"ERC-20 Token Balance: {self.w3.from_wei(balance, 'ether')} tokens")
            await asyncio.sleep(10) #Checks the ERC-20 token balance of an ethereum address every 10 seconds

    def transfer_token(self):
        ''' transfer token based on current balance'''
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

    def start(self):
        ''' starts running behaviours continuously '''
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self.generate_random_message())
        loop.create_task(self.check_balance())
        loop.run_forever()