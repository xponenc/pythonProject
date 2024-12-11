def format_book_data(data: dict) -> str:
    title = data.get("title")
    author = data.get("author")
    genre = data.get("genre")
    return f"Title: {title}, Author: {author}, Genre: {genre}"
