import pytest
import uuid

from app import create_app, db_manager
from app.models import Books, Authors, Genres


@pytest.fixture(scope="function")
def app():
    app = create_app()
    yield app


@pytest.fixture(scope="function")
def client(app):
    with app.app_context():
        yield app.test_client()


# Example: test DB model integrity
def test_books_model(client):
    # initially query the db to find the number of books
    books = Books.query.all()
    books_count_initial = len(books)

    # now insert new entries
    genre_id = uuid.uuid4()
    author_id = 321
    author = Authors(ID=author_id, name="Test Author")
    genre = Genres(ID=genre_id, name="Fiction")
    book = Books(
        ID=123,
        title="Test Book",
        descr="A test book",
        stock=10,
        price=19.99,
        AUTHOR_ID=author_id,
        genre_ID=genre_id,
        currency_code="USD",
        createdBy="tester",
        modifiedBy="tester",
    )
    db_manager.db.session.add_all([author, genre, book])
    db_manager.db.session.commit()

    # query the db again to find the number of books
    books = Books.query.all()
    assert len(books) == books_count_initial + 1

    # cleanup the created entries
    db_manager.db.session.delete(book)
    db_manager.db.session.delete(author)
    db_manager.db.session.delete(genre)
    db_manager.db.session.commit()
