import sqlite3
from contextlib import closing
from functools import wraps

import CONSTANTS


class Repository:
    @staticmethod
    def get_connection():
        return sqlite3.connect(CONSTANTS.DB_FILE_LOCATION, check_same_thread=False)

    @staticmethod
    def create_if_necessary():
        """
        Will open the DB file and create any missing tables, if necessary
        """

        conn = Repository.get_connection()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Chats
        (
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            is_group_chat BOOLEAN NOT NULL CHECK(is_group_chat IN (0, 1))
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Users
        (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            authenticated BOOLEAN NOT NULL CHECK(authenticated IN (0, 1))
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Messages
        (
            sender_username TEXT NOT NULL,
            destination_chat_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            MESSAGE TEXT NOT NULL,
            FOREIGN KEY (sender_username)
                REFERENCES Users (username)
                ON DELETE NO ACTION
                ON UPDATE NO ACTION
            FOREIGN KEY (destination_chat_id)
                REFERENCES Chats (cid)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
            PRIMARY KEY(sender_username, destination_chat_id, timestamp)
        )''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS ChatMembers
        (
            chat_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            FOREIGN KEY (chat_id)
                REFERENCES Chats (cid)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
            FOREIGN KEY (username)
                REFERENCES Users (username)
                ON DELETE CASCADE
                ON UPDATE NO ACTION
            PRIMARY KEY(chat_id, username)
        )''')
        conn.execute('''
        CREATE VIEW IF NOT EXISTS ChatsThatCanAcceptNewMembers
        (cid)
        AS
            SELECT C.cid
            FROM Chats AS C
            INNER JOIN ChatMembers M ON C.cid = M.chat_id
            GROUP BY C.cid, C.is_group_chat
            HAVING C.is_group_chat == "1"
            OR COUNT(*) < 2''')

    @staticmethod
    def db_connect(func):
        """
        Decorator to guarantee a valid connection object in the decorated function
        The connection will be closed after the decorated function returns
        :param Callable func: decorated function
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'connection' not in kwargs:
                kwargs['connection'] = Repository.get_connection()
                with closing(kwargs['connection']):
                    return func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper
