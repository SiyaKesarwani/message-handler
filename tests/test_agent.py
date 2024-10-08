import unittest
from unittest.mock import patch
from queue import Queue
from src.functionalities.concrete_agent import ConcreteAgent

class TestConcreteAgent(unittest.TestCase):
    def setUp(self):
        inbox = Queue()
        outbox = Queue()
        self.agent = ConcreteAgent(inbox, outbox, "Agent")

    @patch('builtins.print')
    def test_handle_hello(self, mock_print):
        # Simulate receiving a message containing "hello"
        message = {'type': 'hello', 'content': 'hello world'}
        self.agent.handle_hello(message, "Agent")
        
        # Check if the print function was called with the correct message
        mock_print.assert_called_once_with("Inbox of Agent (hello) filtered from other's Outbox: hello world")

if __name__ == '__main__':
    unittest.main()
