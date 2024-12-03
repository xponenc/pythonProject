from app_users.exceptions import UserAlreadyExistsError, UserNotFoundError
from app_users.models import UserManager, AuthenticationService, Customer


def main():
    manager = UserManager()

    auth_service = AuthenticationService()
    user_1 = auth_service.register(Customer, "test1", "john@example.com",
                                   "password1", "City Street 1")
    user_2 = auth_service.register(Customer, "test2", "john@example.com",
                                   "password2", "City Street 2")

    try:
        manager.add_user(user_1)
        manager.add_user(user_2)
        manager.add_user(Customer("test2", "john@example.com",
                                  "password2", "City Street 2"))
    except UserAlreadyExistsError as e:
        print(e)

    try:

        manager.remove_user("test1")
        manager.remove_user("user_2")
    except UserNotFoundError as e:
        print(e)

    try:
        found_user = manager.find_user("test2")
        # Попытка найти несуществующего пользователя
        manager.find_user("unknown")
    except UserNotFoundError as e:
        print(e)
    else:
        print(f"Найден пользователь: {found_user}")


if __name__ == "__main__":
    main()
