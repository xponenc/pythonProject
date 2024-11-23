from datetime import datetime

from models import Product, Customer, Order


def test_shop():
    product_1 = Product(name="Товар_1", price=100)
    product_2 = Product(name="Товар_2", price=200)
    print(product_1, product_2)
    print(product_1.__repr__(), product_2.__repr__())
    print(f"{product_1 == product_2=}")
    print(f"{product_1 < product_2=}")
    print(f"{product_1.price=}")
    product_1.price = 200
    print(f"{product_1 == product_2=}")
    product_1.price = 201
    print(f"{product_1 < product_2=}")

    customer_1 = Customer(name="Customer 1")
    customer_2 = Customer(name="Customer 2")

    order_1 = Order()
    order_1.add_product(product_1)
    order_1.add_product(product_2)
    customer_1.add_order(order_1)

    order_2 = Order()
    order_2.add_product(product_2)
    customer_2.add_order(order_2)

    order_3 = Order()
    order_3.add_product(product_2)
    order_3.add_product(product_1)
    customer_2.add_order(order_3)

    print("Общее количество заказов", Order.total_orders())
    print("Общая стоимость заказов", Order.total_orders_cost())
    print(datetime.now())


if __name__ == "__main__":
    test_shop()
