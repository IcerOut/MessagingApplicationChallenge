class User:
    """
    A class containing a user
    Usernames are used as the Primary Key in the DB
    The password will be hashed using bcrypt and used for the authentication optional objective
    The authenticated attribute is used by FlaskLogin
    """
    def __init__(self, username: str or None, password_hash: str or None,
                 authenticated: str or None):
        self.username = username
        self.password_hash = password_hash
        self.authenticated = authenticated

    @classmethod
    def empty(cls):
        return User(None, None, None)

    # <editor-fold desc="FlaskLogin aux functions">
    def is_authenticated(self) -> bool:
        return self.authenticated

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def get_id(self):
        return self.username

    # </editor-fold>

    def __str__(self):
        return 'User{' \
               f'username={self.username}, ' \
               f'password_hash={self.password_hash}, ' \
               f'authenticated={self.authenticated}' \
               '}'

    __repr__ = __str__
