from entities.User import User
from repo.repository import Repository


class UserRepo:
    @Repository.db_connect
    def create_user(self, new_user: User, connection=None) -> None:
        cursor = connection.cursor()
        cursor.execute(
                'INSERT INTO Users (username, password_hash, authenticated)'
                'VALUES (?, ?, ?)',
                (new_user.username, new_user.password_hash, new_user.authenticated))
        connection.commit()

    @Repository.db_connect
    def get_user(self, username: str, connection=None) -> User or None:
        cursor = connection.cursor()
        cursor.execute('SELECT password_hash, authenticated '
                       'FROM Users '
                       'WHERE username = ?', (username,))
        try:
            row = cursor.fetchall()[0]
            return User(username, password_hash=row[0], authenticated=row[1])
        except IndexError:
            return None

    @Repository.db_connect
    def update_authenticated_status(self, username: str, authenticated: bool,
                                    connection=None) -> None:
        cursor = connection.cursor()
        cursor.execute(
                'UPDATE Users '
                'SET authenticated = ?'
                'WHERE username = ?', (
                    authenticated, username))
        connection.commit()
