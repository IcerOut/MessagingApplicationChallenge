import bcrypt

from entities.User import User
from repo.UserRepo import UserRepo


class UserController:
    def __init__(self):
        self.repo = UserRepo()

    def _hash_password(self, password: str) -> str:
        """
        Hashes a password for storing in the DB
        :param password: Unhashed password
        :return: The same password, hashed and salted using bcrypt
        """
        return bcrypt.hashpw(password.encode('utf-8'),
                             bcrypt.gensalt()).decode('utf-8')

    def exists(self, username: str) -> bool:
        return self.repo.get_user(username) is not None

    def get_by_username(self, username: str) -> User or None:
        return self.repo.get_user(username)

    def create(self, username: str, password: str) -> None:
        self.repo.create_user(User(username, self._hash_password(password), False))

    def update_authenticated_status(self, username: str, authenticated: bool) -> None:
        self.repo.update_authenticated_status(username, authenticated)

    def is_auth_valid(self, username: str, password: str) -> bool:
        """
        Checks whether a certain username/password combination is correct
        """
        user = self.repo.get_user(username)
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return True
            else:
                return False
        else:
            return False
