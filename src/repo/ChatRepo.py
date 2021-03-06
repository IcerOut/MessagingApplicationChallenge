import logging
import sqlite3

from entities.Chat import Chat
from repo.Repository import Repository


class ChatRepo:
    @Repository.db_connect
    def create_chat(self, is_group_chat: bool, connection=None) -> int:
        """
        Create a new group chat and add the creator as the first member
        :param is_group_chat: Whether the new chat is a group or p2p chat
        :param connection: DB Connection
        :param connection: The automatically-managed connection object
        :return: The ID of the newly created group chat
        """
        cursor = connection.cursor()
        cursor.execute(
                'INSERT INTO Chats (is_group_chat) '
                'VALUES (?) ', (int(is_group_chat),))
        new_chat_id = cursor.lastrowid
        connection.commit()
        return new_chat_id

    @Repository.db_connect
    def get_chat_by_id(self, cid: int, connection=None) -> Chat or None:
        cursor = connection.cursor()
        cursor.execute('SELECT cid, is_group_chat '
                       'FROM Chats '
                       'WHERE cid = ?', (cid,))
        try:
            row = cursor.fetchall()[0]
            return Chat(cid=row[0], is_group_chat=bool(row[1]))
        except IndexError:
            return None

    @Repository.db_connect
    def get_chat_by_members(self, member1: str, member2: str, connection=None) -> Chat or None:
        cursor = connection.cursor()
        cursor.execute('SELECT C.cid '
                       'FROM Chats AS C '
                       'INNER JOIN ChatMembers AS M1 ON C.cid = M1.chat_id '
                       'INNER JOIN ChatMembers AS M2 ON C.cid = M2.chat_id '
                       'WHERE C.is_group_chat == "0" AND M1.username = ? AND M2.username = ?',
                       (member1, member2))
        try:
            row = cursor.fetchall()[0]
            return Chat(cid=row[0], is_group_chat=False)
        except IndexError:
            return None

    @Repository.db_connect
    def add_user_to_chat(self, cid: int, username: str, connection=None) -> bool:
        """
        Attempts to add a user to a chat
        :param cid: The chat to which the user will be added
        :param username: The user to be added
        :param connection: The automatically-managed connection object
        :return: True on success, False on failure
        """
        cursor = connection.cursor()
        try:
            cursor.execute(
                    'INSERT INTO ChatMembers (chat_id, username)'
                    'VALUES (?, ?)',
                    (cid, username))
            connection.commit()
            return True
        except sqlite3.Error as err:
            logging.error(err)
            return False

    @Repository.db_connect
    def delete_user_from_chat(self, cid: int, username: str, connection=None) -> bool:
        """
        Attempts to delete a user from a chat
        :param cid: The chat from which the user will be deleted
        :param username: The user to be deleted
        :param connection: The automatically-managed connection object
        :return: True on success, False on failure
        """
        cursor = connection.cursor()
        try:
            cursor.execute(
                    'DELETE FROM ChatMembers '
                    'WHERE chat_id = ? AND username = ?',
                    (cid, username))
            connection.commit()
            return True
        except sqlite3.Error as err:
            logging.error(err)
            return False

    @Repository.db_connect
    def can_accept_new_members(self, cid: int, connection=None) -> bool:
        cursor = connection.cursor()
        cursor.execute('SELECT * '
                       'FROM ChatsThatCanAcceptNewMembers '
                       'WHERE cid == ?', (cid,))
        try:
            row = cursor.fetchall()[0]
            return row[0] is not None
        except IndexError:
            return False

    @Repository.db_connect
    def is_member(self, cid: int, username: str, connection=None) -> bool:
        cursor = connection.cursor()
        cursor.execute('SELECT *'
                       'FROM ChatMembers '
                       'WHERE chat_id = ? AND username = ?', (cid, username))
        try:
            row = cursor.fetchall()[0]
            return row[0] is not None
        except IndexError:
            return False
