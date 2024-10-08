class Agent:
    '''
    This is Parent Agent class which is responsible for 
    processing Inbox of Agents.
    '''
    def __init__(self, inbox, outbox, name):
        self.name = name
        self.inbox = inbox
        self.outbox = outbox
        self.handlers = {}

    def register_handler(self, message_type, handler):
        ''' Parent has info of all handlers '''
        self.handlers[message_type] = handler

    def emit_message(self, message):
        ''' Setting Outbox message '''
        self.outbox.put(message)

    def process_inbox(self):
        ''' Process Inbox messages '''
        while True:
            message = self.inbox.get()
            if message is None:  # Shutdown signal
                break
            message_type = message.get('type')
            if message_type in self.handlers:
                self.handlers[message_type](message, self.name)