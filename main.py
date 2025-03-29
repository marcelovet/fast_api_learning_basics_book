from typing import Any

from fastapi import FastAPI

# from fastapi import Body
from mock_data import create_mock_book
from models import Book, BookRequest

app = FastAPI()

BOOKS: list[Book] = [create_mock_book(i) for i in range(1, 100)]


def fetch_by(param: dict[str, Any], query: list[dict[str, Any] | None] = []):
    books_to_return: list[Book] = []
    books_to_return.extend(
        book
        for book in BOOKS
        if book.model_dump().get(param["name"], "").casefold()
        == param["value"].casefold()
    )
    if not books_to_return:
        return []
    if not query:
        return books_to_return
    for query_param in query:
        if books_to_return and query_param:
            books_to_return = [
                book
                for book in books_to_return
                if book.model_dump().get(query_param["name"], "").casefold()
                == query_param["value"].casefold()
            ]
    if not books_to_return:
        return []
    return books_to_return


@app.get("/books")
async def get_books():
    return BOOKS


@app.get("/books/{id}")
async def get_book(id: int):
    if id and id > 0 and id <= len(BOOKS):
        return BOOKS[id - 1]
    return []


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


@app.post("/books/create")
async def create_book(request: BookRequest):
    new_id = BOOKS[-1].id + 1 if BOOKS else 1
    new_book = Book(id=new_id, **request.model_dump())
    BOOKS.append(new_book)


# @app.put("/books/update")
# async def update_book(updated_book=Body()):
#     for i in range(len(BOOKS)):
#         if BOOKS[i].get("title", "").casefold() == updated_book.get("title").casefold():
#             BOOKS[i] = updated_book
#             break


# @app.delete("/books/delete/{book_title}")
# async def delete_book(book_title: str):
#     for i in range(len(BOOKS)):
#         if BOOKS[i].get("title", "").casefold() == book_title.casefold():
#             BOOKS.pop(i)
#             break
