from .utils.data_validation import validate_book_data


class Author:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name


class Genre:
    def __init__(self, name):
        self.__name = name
        self.__books = []

    @property
    def name(self):
        return self.__name


class Book:
    def __init__(self, title, author, genre):
        self.__title = title
        self.__author = Author(name=author)
        self.__genre = Genre(name=genre)

    def __str__(self):
        return f"{self.__title} {self.__author.name} {self.__genre.name}"

    @property
    def title(self):
        return self.__title

    @property
    def author(self):
        return self.__author

    @property
    def genre(self):
        return self.__genre


class ValidationError(Exception):
    pass


class Library:

    def __init__(self, name):
        self.__name = name
        self.__books = {}

    def __str__(self):
        return f"{self.__name} - {len(self.__books)}"

    def add_book(self, title, author, genre):
        is_valid = validate_book_data({"title": title, "author": author, "genre": genre})
        if not is_valid:
            raise ValidationError(f"Данные некорректны {title, author, genre}")
        self.__books[title] = Book(title, author, genre)

    def delete_book(self, title):
        try:
            del self.__books[title]
            print("Книга удалена")
        except KeyError:
            print("Книга не найден")

    def search_book(self, query):
        result = set(str(book) for book in self.__books.values() if query.lower() in str(book).lower())
        if not result:
            result = "Ничего не найдено"
        return result

    def catalog(self, verbose=True):
        if not verbose:
            return self.__books.values()
        for book in self.__books.values():
            print(book)
