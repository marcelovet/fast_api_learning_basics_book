from typing import Any

from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author One", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]


@app.get("/books")
async def books():
    return BOOKS


@app.get("/books/category/{book_category}")
async def book(book_category: str, title: str | None = None, author: str | None = None):
    books_to_return: list[dict[str, Any]] = []
    books_to_return.extend(
        book
        for book in BOOKS
        if book.get("category", "").casefold() == book_category.casefold()
    )
    if not books_to_return:
        return {"title": None, "author": None, "category": None}
    if books_to_return and title:
        books_to_return = [
            book
            for book in books_to_return
            if book.get("title", "").casefold() == title.casefold()
        ]
    if books_to_return and author:
        books_to_return = [
            book
            for book in books_to_return
            if book.get("author", "").casefold() == author.casefold()
        ]
    if not books_to_return:
        return {"title": None, "author": None, "category": None}
    return books_to_return
