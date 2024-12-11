from .utils.formatting import format_book_data
from .catalog import Library


def generate_report(library: Library):
    report = "; ".join(map(format_book_data,
                           [{"title": book.title, "author": book.author.name, "genre": book.genre.name}
                            for book in library.catalog(verbose=False)])
                       )
    return report

