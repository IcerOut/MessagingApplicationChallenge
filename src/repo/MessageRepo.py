from datetime import datetime
from typing import List

from entities.Message import Message
from repo.Repository import Repository


class MessageRepo:
    @Repository.db_connect
    def send_message(self, sender_username: str, cid: int, message: str, connection=None) -> None:
        """
        Send a message to a chat
        The timestamp is automatically set to the current moment ("now")
        :param sender_username: The username of the sender
        :param cid: The ID of the chat where the message should be sent
        :param message: The content of the message
        :param connection: The automatically-managed connection object
        """
        cursor = connection.cursor()
        cursor.execute(
                'INSERT INTO Messages (sender_username, destination_chat_id, timestamp, message) '
                'VALUES (?, ?, datetime("now", "localtime"), ?)', (sender_username, cid, message))
        connection.commit()

    @Repository.db_connect
    def get_chat_messages(self, cid: int, connection=None) -> List[Message]:
        cursor = connection.cursor()
        cursor.execute('SELECT sender_username, destination_chat_id, timestamp, message '
                       'FROM Messages '
                       'WHERE destination_chat_id = ?', (cid,))
        message_list = []
        try:
            results = cursor.fetchall()
            for row in results:
                message_list.append(Message(sender_username=row[0], destination_chat_id=row[1],
                                            timestamp=datetime.strptime(row[2],
                                                                        '%Y-%m-%d %H:%M:%S'),
                                            message=row[3]))
            return message_list
        except IndexError:
            return message_list

    @Repository.db_connect
    def get_user_messages(self, username: str, connection=None) -> List[Message]:
        cursor = connection.cursor()
        cursor.execute('SELECT sender_username, destination_chat_id, timestamp, message '
                       'FROM Messages AS M '
                       'INNER JOIN ChatMembers AS CM ON M.destination_chat_id = CM.chat_id '
                       'WHERE CM.username = ?', (username,))
        message_list = []
        try:
            results = cursor.fetchall()
            for row in results:
                message_list.append(Message(sender_username=row[0], destination_chat_id=row[1],
                                            timestamp=datetime.strptime(row[2],
                                                                        '%Y-%m-%d %H:%M:%S'),
                                            message=row[3]))
            return message_list
        except IndexError:
            return message_list
