# Message Handler Agents

## Overview

This project implements an autonomous agent in Python that interacts with the Ethereum blockchain. The agent is designed to continuously consume messages, emit messages, register handlers for processing various message types, and execute proactive behaviors based on its internal state and local time.

## Features

- **Message Handling**: The agent can receive messages from an inbox and process them using registered handlers.
- **Proactive Behavior**: The agent generates random 2-word messages at regular intervals and checks the ERC-20 token balance of a specified Ethereum address.
- **Ethereum Interaction**: Using the `web3.py` library, the agent can check token balances and transfer tokens between addresses based on message content.
- **Inter-Agent Communication**: Two instances of the agent can communicate with each other, where the inbox of one agent serves as the outbox of another.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SiyaKesarwani/message-handler.git
   cd message-handler
   ```

2. **Install Dependencies**:

    To install Python 3, follow the instructions for your operating system:

- **Windows**:
  1. Download the installer from the [official Python website](https://www.python.org/downloads/).
  2. Run the installer and ensure that the option "Add Python to PATH" is selected.
  
- **macOS**:
  1. You can use Homebrew to install Python. Open a terminal and run:
     ```bash
     brew install python3
     ```

- **Linux**:
  1. You can install Python using your package manager. For example, on Ubuntu:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip
     ```



    To install required packages for project:
   ```bash
   pip install web3
   pip install python-dotenv
   ```

3. **Configuration**:
   - Update the `INFURA_URL`, `TOKEN_ADDRESS`, `SOURCE_ADDRESS`, `TARGET_ADDRESS`, and `PRIVATE_KEY` in the code with your actual Ethereum details.
   - Optionally, set up a dedicated [Tenderly](https://tenderly.co/) fork for safe testing.

## Usage

1. **Run the Agent**:
   Execute the script to start the agent instances. They will begin communicating with each other and interacting with the Ethereum blockchain.

   ```bash
   python3 src/index.py
   ```

2. **Monitor Output**:
   The agents will print their activities to stdout, including generated messages, token balance checks, and transfer confirmations.

## Testing

- Unit tests are provided to validate individual components of the agent.
- Integration tests ensure that the agents communicate and process messages correctly.

To run all the tests, use:

```bash
python3 -m unittest
```

## Acknowledgments

- [Tenderly](https://tenderly.co/) for providing a platform to test and debug Ethereum smart contracts.
- [web3.py](https://web3py.readthedocs.io/en/stable/) for simplifying Ethereum interactions in Python.