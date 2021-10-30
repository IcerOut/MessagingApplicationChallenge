class Chat:
    """
    A class containing a chat (either group or P2P)
    The CID represents a unique ID for the chat
    """

    def __init__(self, cid: int or None, is_group_chat: bool or None):
        self.cid = cid
        self.is_group_chat = is_group_chat

    @classmethod
    def empty(cls):
        return Chat(None, None)

    def __str__(self):
        return 'Chat{' \
               f'cid={self.cid}, ' \
               f'is_group_chat={self.is_group_chat}' \
               '}'

    __repr__ = __str__
