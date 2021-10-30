from typing import List

from entities.Message import Message
from entities.User import User


class Chat:
    """
    A class containing a chat (either group or P2P)
    The CID represents a unique ID for the chat
    The participants represents a list of User objects, all of the participants of the chat
    The messages represents a list of Message objects, all of the messages sent in this chat
    """
    def __init__(self, cid: int or None, participants: List[User] or None,
                 messages: List[Message] or None):
        self.cid = cid
        self.participants = participants
        self.messages = messages

    @classmethod
    def empty(cls):
        return Chat(None, None, None)

    def __str__(self):
        return 'Chat{' \
               f'cid={self.cid}, ' \
               f'participants={self.participants}, ' \
               f'messages={self.messages}, ' \
               '}'

    __repr__ = __str__
