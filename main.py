from datetime import datetime

from app_shop.models import Product


def test_shop():
    product_1 = Product(name="Товар_1", price=100)
    product_2 = Product(name="Товар_2", price=200)


if __name__ == "__main__":
    test_shop()
