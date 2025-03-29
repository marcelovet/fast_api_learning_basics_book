from pydantic import BaseModel, Field


class Book(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=10)
    category: str = Field(min_length=4)
    rating: int = Field(gt=-1, lt=6)


class BookRequest(BaseModel):
    title: str = Field(
        min_length=3,
        description=(
            "The title of the book, which has to be at least 3 characters long."
        ),
    )
    author: str = Field(
        min_length=3,
        description=("The author of the book."),
    )
    description: str = Field(
        min_length=10,
        description=("The description of the book."),
    )
    category: str = Field(
        min_length=4,
        description=("The category of the book."),
    )
    rating: int = Field(
        gt=-1,
        lt=6,
        description="The rating of the book.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "description": (
                    "The story primarily concerns the young and mysterious "
                    "millionaire Jay Gatsby and his quixotic passion and "
                    "obsession with the beautiful former debutante "
                    "Daisy Buchanan."
                ),
                "category": "Fiction",
                "rating": 4,
            }
        }
    }
