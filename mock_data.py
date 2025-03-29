from random import choice

from faker import Faker

from models import Book

fake = Faker("pt_BR")

genres = [
    "Fiction",
    "Mystery",
    "Romance",
    "Science",
    "History",
    "Biography",
    "Fantasy",
    "Horror",
    "Adventure",
    "Drama",
    "Poetry",
    "Philosophy",
    "Contemporary",
    "Classic",
    "Young Adult",
    "Children",
    "Thriller",
    "Self-Help",
    "Business",
    "Technology",
]


def create_mock_book(id: int) -> Book:
    return Book(
        id=id,
        title=fake.sentence(nb_words=3),
        author=fake.name(),
        description=fake.sentence(nb_words=10),
        category=choice(genres),
        rating=fake.random_int(min=1, max=5),
    )
