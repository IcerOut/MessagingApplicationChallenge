class Chat:
    """
    A class containing a chat (either group or P2P)
    The CID represents a unique ID for the chat
    """

    def __init__(self, cid: int or None):
        self.cid = cid

    @classmethod
    def empty(cls):
        return Chat(None)

    def __str__(self):
        return 'Chat{' \
               f'cid={self.cid}' \
               '}'

    __repr__ = __str__
