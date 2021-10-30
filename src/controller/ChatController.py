from entities.Chat import Chat
from repo.ChatRepo import ChatRepo


class ChatController:
    def __init__(self):
        self.repo = ChatRepo()

    def is_member(self, cid: int, username: str) -> bool:
        return self.repo.is_member(cid=cid, username=username)

    def exists(self, cid: int) -> bool:
        return self.repo.get_chat_by_id(cid) is not None

    def get_by_id(self, cid: int) -> Chat or None:
        return self.repo.get_chat_by_id(cid)

    def get_p2p_by_members(self, member1: str, member2: str) -> Chat or None:
        return self.repo.get_chat_by_members(member1, member2)

    def create_group_chat(self, owner_username: str) -> int:
        new_chat_id = self.repo.create_chat(True)
        self.repo.add_user_to_chat(cid=new_chat_id, username=owner_username)
        return new_chat_id

    def create_p2p_chat(self, sender_username: str, dest_username: str) -> None:
        new_chat_id = self.repo.create_chat(False)
        self.repo.add_user_to_chat(cid=new_chat_id, username=sender_username)
        self.repo.add_user_to_chat(cid=new_chat_id, username=dest_username)

    def add_user_to_chat(self, cid: int, username: str) -> bool:
        if not self.repo.can_accept_new_members(cid=cid):
            raise ValueError('You cannot add members to a P2P chat!')
        return self.repo.add_user_to_chat(cid=cid, username=username)

    def delete_user_from_chat(self, cid: int, username: str) -> bool:
        return self.repo.delete_user_from_chat(cid=cid, username=username)