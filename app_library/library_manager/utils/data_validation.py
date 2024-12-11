def validate_book_data(data: dict) -> bool:
    title = data.get("title")
    author = data.get("author")
    genre = data.get("genre")
    if not all((title, author, genre)):
        return False
    return True
