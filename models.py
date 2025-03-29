from pydantic import BaseModel, Field


class Book(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=10)
    category: str = Field(min_length=4)
    rating: int = Field(gt=-1, lt=6)


class BookRequest(BaseModel):
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=10)
    category: str = Field(min_length=4)
    rating: int = Field(gt=-1, lt=6)
