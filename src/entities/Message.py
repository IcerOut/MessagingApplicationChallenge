from datetime import datetime


class Message:
    """
    A class containing a message
    The Sender is a user ID
    The Destination is a chat ID (P2P chats are just a group chat with 2 users)
    The timestamp is the time the message was send
    The message is the content of the message
    The DB Primary Key is (sender_user_id, destination_chat_id, timestamp)
    """

    def __init__(self, sender_username: str or None, destination_chat_id: int or None,
                 timestamp: datetime or None, message: str or None):
        self.sender_username = sender_username
        self.destination_chat_id = destination_chat_id
        self.timestamp = timestamp
        self.message = message

    @classmethod
    def empty(cls):
        return Message(None, None, None, None)

    def __str__(self):
        return 'Message{' \
               f'sender_username={self.sender_username}, ' \
               f'destination_chat_id={self.destination_chat_id}, ' \
               f'timestamp={self.timestamp}, ' \
               f'message={self.message}' \
               '}'

    __repr__ = __str__
