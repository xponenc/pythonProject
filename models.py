class Product:
    """Модель Продукта"""

    def __init__(self, name: str, price: float):
        self.__name = name
        self.__price = price

    def __str__(self):
        return f"Продукт {self.__name} (цена={self.__price})"

    def __repr__(self):
        return f"Product(name={self.__name}, price={self.__price})"

    @property
    def price(self):
        return self.__price

    # свойство-сеттер
    @price.setter
    def price(self, new_price):
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не может быть отрицательной")

    def __eq__(self, other):
        return self.__price == other.__price

    def __lt__(self, other):
        return self.__price < other.__price


class Customer:
    """Модель Покупателя"""

    def __init__(self, name: str):
        self.__name = name
        self.__orders = list()

    def __str__(self):
        return f"Покупатель {self.__name}"

    def __repr__(self):
        return f"Customer(name={self.__name}"

    def add_order(self, order):
        if order not in self.__orders:
            self.__orders.append(order)

    def order_history(self):
        history = "\n".join(str(order) for order in self.__orders)
        print(f"История заказов:\n{history}\n")


class Order:
    """Класс Order"""
    __total_orders = 0
    __total_orders_cost = 0

    def __init__(self, products: list = None):
        self.__id = Order.__total_orders
        self.__products = products if products else []
        Order.__total_orders += 1
        if products:
            Order.__total_orders_cost += self.total_price()

    def __str__(self):
        return (f"Заказ id {self.__id}\n\t{'\n\t'.join(str(product) for product in self.__products)}"
                f"\nИТОГО {self.total_price()}\n")

    def __repr_(self):
        return f"Order(products={self.__products})"

    def total_price(self):
        return sum(product.price for product in self.__products)

    def add_product(self, product):
        self.__products.append(product)
        Order.__total_orders_cost += product.price

    @classmethod
    def total_orders(cls):
        return cls.__total_orders

    @classmethod
    def total_orders_cost(cls):
        return cls.__total_orders_cost


class Discount:
    """Модель скидки"""
    def __init__(self, description: str, discount_percent: int):
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Скидка должна быть в диапазоне от 0 до 100")
        self.__description = description
        self.__discount_percent = discount_percent

    @property
    def discount_percent(self):
        return self.__discount_percent

    def __str__(self):
        return f"Скидка {self.__description} {self.__discount_percent}%"

    def __repr_(self):
        return f"Discount(description={self.__description}, discount_percent={self.__discount_percent})"

    def apply_to_order(self, order):
        """Применяет текущую скидку ко всему заказу"""
        return sum(
            self.apply_discount(product.price, self.__discount_percent)
            for product in order.products
        )

    @staticmethod
    def apply_discount(price, discount_percent):
        """Применяет процентную скидку к цене"""
        return price * (1 - discount_percent / 100)

    @staticmethod
    def seasonal_discount(price, season):
        """Применяет сезонную скидку в зависимости от текущего сезона."""
        seasonal_discounts = {
            "summer": 15,
            "winter": 10,
            "spring": 5,
            "autumn": 20,
        }
        discount_percent = seasonal_discounts.get(season.lower(), 0)
        return price * (1 - discount_percent / 100)

    @staticmethod
    def promo_code_discount(price, promo_code):
        """ Применяет скидку по промокоду"""
        promo_codes = {
            "SAVE10": 10,
            "BIGSALE": 20,
            "FREESHIP": 5,
        }
        discount_percent = promo_codes.get(promo_code.upper(), 0)
        return price * (1 - discount_percent / 100)
