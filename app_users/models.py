from pprint import pprint

from passlib.hash import sha256_crypt

from app_users.exceptions import UserAlreadyExistsError, UserNotFoundError


class User:
    """Модель Пользователь"""
    users = dict()

    def __init__(self, username, email, password, age=None):
        self.__username = username
        self.__email = email
        self.__age = age
        self.__password = self.hash_password(password)
        User.users[self.__username] = self

    def __str__(self):
        return self.__username

    def __repr__(self):
        return f"""{self.__class__.__name__}({', '.join(f'{key.split("__")[-1]}="{value}"' for key, value in self.__dict__.items())})"""

    @property
    def username(self):
        return self.__username

    @staticmethod
    def hash_password(password):
        return sha256_crypt.using(rounds=5000).hash(password)

    def check_password(self, provided_password):
        return sha256_crypt.verify(provided_password, self.__password)

    def get_details(self):
        return {
            "username": self.__username,
            "email": self.__email,
            "role": self.__class__.__name__
        }


class Customer(User):
    """Модель Покупатель"""

    def __init__(self, username, email, password, address):
        super().__init__(username, email, password)
        self.__address = address

    def get_details(self):
        details = super().get_details()
        details["address"] = self.__address
        return details


class Admin(User):
    """Модель Администратор"""

    def __init__(self, username, email, password, admin_level):
        super().__init__(username, email, password)
        self.admin_level = admin_level

    def get_details(self):
        details = super().get_details()
        details["admin_level"] = self.admin_level
        return details

    @staticmethod
    def list_users():
        return [_user.get_details() for _user in User.users.values()]

    @staticmethod
    def delete_user(username):
        if username in User.users:
            User.users.pop(username)
            # TODO Надо удалять из списка аутентифицированных
            print(f"Пользователь {username} удален.")
            return True
        print(f"Пользователь {username} не найден.")


class AuthenticationService:
    """Модель аутентификации и авторизации пользователй"""

    def __init__(self):
        self.__logged_users = []

    @classmethod
    def register(cls, user_class, username, email, password, *args):
        if username in User.users:
            print(f"Имя пользователя {username} уже занято.")
            return False
        user = user_class(username, email, password, *args)
        print(f"Пользователь {username} успешно зарегистрирован.")
        return user

    def login(self, username, password):
        checked_user = User.users.get(username)
        if not checked_user or not checked_user.check_password(password):
            print("Неправильные логин или пароль")
            return False
        if username in self.__logged_users:
            print(f"Пользователь {username} уже вошел в систему из другого места.")
            return False
        self.__logged_users.append(username)
        print(f"Пользователь {username} успешно вошел в систему.")
        return True

    def logout(self, username):
        if username not in self.__logged_users:
            print("Ошибка. Пользователь не входил в систему")
            return False

        self.__logged_users.remove(username)
        print(f"Пользователь {username} успешно вышел из системы.")
        return True

    def get_logged_users(self):
        return self.__logged_users


class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user: User):
        if user.username in self.users:
            raise UserAlreadyExistsError(f"Пользователь '{user.username}' уже существует")
        self.users[user.username] = user
        print(f"Пользователь '{user.username}' успешно добавлен")

    def remove_user(self, username: str):
        if username not in self.users:
            raise UserNotFoundError(f"Пользователь '{username}' не найден.")
        del self.users[username]
        print(f"Пользователь '{username}' успешно удален")

    def find_user(self, username: str) -> User:
        if username not in self.users:
            raise UserNotFoundError(f"Пользователь '{username}' не найден.")
        return self.users[username]


if __name__ == "__main__":
    auth_service = AuthenticationService()

    auth_service.register(Customer, "test2", "john@example.com", "password2", "City Street 1")
    auth_service.login("test2", "password2")
    auth_service.logout("test2")
    admin = User.users.get("admin_user")
    admin.delete_user("test3")

