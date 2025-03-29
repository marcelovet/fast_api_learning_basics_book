from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    category: str
    rating: int
