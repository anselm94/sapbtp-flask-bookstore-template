import logging

from app import db_manager
from app.models import Books, Authors, Currencies, Genres

log = logging.getLogger("route-books")

db = db_manager.db


def get_books():
    """
    Fetches all books from the database and returns them as a list of dictionaries.
    """
    log.info("Fetching books from the database...")
    books = db.session.execute(
        db.select(
            Books.ID,
            Books.title,
            Books.descr,
            Books.stock,
            Books.price,
            Currencies.code.label("currency_code"),
            Currencies.symbol.label("currency_symbol"),
            Authors.name.label("author_name"),
            Genres.name.label("genre"),
        )
        .join(Books.author)  # Explicit join to Authors
        .join(Books.currency)  # Explicit join to Currencies
        .join(Books.genre)  # Explicit join to Genres
        .order_by(Books.title)
    ).all()
    log.info(f"Fetched {len(books)} books from the database.")

    if not books:
        log.warning("No books found in the database.")
        return []

    return [
        {
            "id": book.ID,
            "title": book.title,
            "descr": book.descr,
            "stock": book.stock,
            "price": {
                "value": book.price,
                "currency": {
                    "code": book.currency_code,
                    "symbol": book.currency_symbol,
                },
            },
            "author": book.author_name,
            "genre": book.genre,
        }
        for book in books
    ]
