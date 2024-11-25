from pprint import pprint

from passlib.hash import sha256_crypt


class User:
    """Модель Пользователь"""
    users = dict()

    def __init__(self, username, email, password):
        self.__username = username
        self.__email = email
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

    #
    # def add_order(self, order):
    #     if order not in self.__orders:
    #         self.__orders.append(order)
    #
    # def order_history(self):
    #     history = "\n".join(str(order) for order in self.__orders)
    #     print(f"История заказов:\n{history}\n")


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
            return True
        user_class(username, email, password, *args)
        print(f"Пользователь {username} успешно зарегистрирован.")

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


if __name__ == "__main__":
    auth_service = AuthenticationService()

    print("\n", 5 * "*", "Регистрация")
    auth_service.register(Customer, "test2", "john@example.com", "password2", "City Street 1")
    auth_service.register(Customer, "test2", "john@example.com", "password2", "City Street 1")
    auth_service.register(Customer, "test3", "john@example.com", "password3", "City Street 2")
    auth_service.register(Admin, "admin_user", "admin@example.com", "pass", 1)

    print("\n", 5 * "*", "Аутентификация")
    auth_service.login("test2", "password21")
    auth_service.login("test2", "password2")
    auth_service.login("test3", "password3")
    auth_service.login("admin_user", "pass")
    auth_service.login("admin_user", "pass")
    print(auth_service.get_logged_users())

    print("\n", 5 * "*", "Выход из системы")
    auth_service.logout("test2")
    print(auth_service.get_logged_users())

    print("\n", 5 * "*", "Действия админа")
    admin = User.users.get("admin_user")
    admin.delete_user("test3")
    print(admin.list_users())
