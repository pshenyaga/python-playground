from aiohttp.log import server_logger

class User:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self._password = password

    def __repr__(self):
        template = 'User name={s.name}: <{s.email}>'
        return template.format(s=self)

    def match_password(self, password: str):
        if self._password != password:
            raise self.PasswordDoesNotMatch("Wrong password")

    class PasswordDoesNotMatch(Exception):
        pass

class UserStorage:
    _users = []

    @classmethod
    def add_user(cls, name: str, email: str, password: str):
        try:
            cls.get_user(name=name, email=email)
            raise cls.UserAlreadyExists            

        except cls.UserNotFound:
            cls._users.append(
                User(name, email, password))

    @classmethod
    def get_user(cls, **kwargs):
        users = cls._users
        for k, v in kwargs.items():
            users = [u for u in users if getattr(u, k, None) == v]

        if len(users) == 0:
            raise cls.UserNotFound("User not found")

        return users[0]

    class UserNotFound(Exception):
        pass

    class UserAlreadyExists(Exception):
        pass

def create_example_storage():
    UserStorage.add_user('user1', 'user1.example.com', '111111')
    UserStorage.add_user('user2', 'user2.example.com', '222222')