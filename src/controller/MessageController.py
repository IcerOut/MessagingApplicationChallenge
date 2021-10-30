from typing import List

from entities.Message import Message
from repo.MessageRepo import MessageRepo


class MessageController:
    def __init__(self):
        self.repo = MessageRepo()

    def send_message(self, sender_username: str, cid: int, message: str) -> None:
        self.repo.send_message(sender_username=sender_username, cid=cid, message=message)

    def get_chat_messages(self, cid: int) -> List[Message]:
        return self.repo.get_chat_messages(cid=cid)

    def get_user_messages(self, username: str) -> List[Message]:
        return self.repo.get_user_messages(username=username)
