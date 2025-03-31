from datetime import date
from typing import Any

from fastapi import FastAPI, Path

from mock_data import create_mock_book
from models import Book, BookRequest

app = FastAPI()

BOOKS: list[Book] = [create_mock_book(i) for i in range(1, 100)]


def fetch(to_filter: list[Book], name: str, value: Any):
    if not to_filter:
        return []
    if isinstance(value, str):
        return [
            book
            for book in to_filter
            if book.model_dump().get(name, "").casefold() == value.casefold()
        ]
    if isinstance(value, int):
        return [book for book in to_filter if book.model_dump().get(name, 0) == value]
    if isinstance(value, date):
        return [
            book
            for book in to_filter
            if name in book.model_dump() and book.model_dump()[name].year == value.year
        ]
    return []


def fetch_by(param: dict[str, Any], query: list[dict[str, Any] | None] = []):
    books_to_return: list[Book] = fetch(BOOKS, param["name"], param["value"])
    if not books_to_return or not query:
        return books_to_return
    for query_param in query:
        if query_param:
            books_to_return = fetch(
                books_to_return, query_param["name"], query_param["value"]
            )
    return books_to_return


@app.get("/books")
async def get_books():
    return BOOKS


@app.get("/books/{id}")
async def get_book(id: int = Path(gt=0)):
    return fetch_by({"name": "id", "value": id})


@app.get("/books/category/{category}")
async def get_books_by_category(
    category: str, title: str | None = None, author: str | None = None
):
    return fetch_by(
        {"name": "category", "value": category},
        [
            {"name": "title", "value": title} if title else None,
            {"name": "author", "value": author} if author else None,
        ],
    )


@app.get("/books/title/{title}")
async def get_books_by_title(
    title: str, category: str | None = None, author: str | None = None
):
    return fetch_by(
        {"name": "title", "value": title},
        [
            {"name": "category", "value": category} if category else None,
            {"name": "author", "value": author} if author else None,
        ],
    )


@app.get("/books/author/{author}")
async def get_books_by_author(
    author: str, category: str | None = None, title: str | None = None
):
    return fetch_by(
        {"name": "author", "value": author},
        [
            {"name": "category", "value": category} if category else None,
            {"name": "title", "value": title} if title else None,
        ],
    )


@app.get("/books/rating/{rating}")
async def get_books_by_rating(
    rating: int,
    author: str | None = None,
    category: str | None = None,
    title: str | None = None,
):
    return fetch_by(
        {"name": "rating", "value": rating},
        [
            {"name": "author", "value": author} if author else None,
            {"name": "category", "value": category} if category else None,
            {"name": "title", "value": title} if title else None,
        ],
    )


@app.get("/books/publication_year/{year}")
async def get_books_by_publication_year(
    year: int,
    rating: int | None = None,
    author: str | None = None,
    category: str | None = None,
    title: str | None = None,
):
    return fetch_by(
        {"name": "published_date", "value": date(year, 1, 1)},
        [
            {"name": "rating", "value": rating} if rating else None,
            {"name": "author", "value": author} if author else None,
            {"name": "category", "value": category} if category else None,
            {"name": "title", "value": title} if title else None,
        ],
    )


@app.post("/books/create")
async def create_book(request: BookRequest):
    request.id = BOOKS[-1].id + 1 if BOOKS else 1
    new_book = Book(**request.model_dump())
    BOOKS.append(new_book)


@app.put("/books/update")
async def update_book(request: BookRequest):
    book = fetch_by({"name": "id", "value": request.id})
    if not book:
        return {"message": "Book not found"}
    book[0].title = request.title
    book[0].author = request.author
    book[0].description = request.description
    book[0].category = request.category
    book[0].rating = request.rating
    return book[0]


@app.delete("/books/delete/{id}")
async def delete_book(id: int = Path(gt=0)):
    book = fetch_by({"name": "id", "value": id})
    if not book:
        return {"message": "Book not found"}
    BOOKS.remove(book[0])
