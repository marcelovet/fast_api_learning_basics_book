from faker import Faker

from models import Book

fake = Faker("pt_BR")


def create_mock_book(id: int) -> Book:
    return Book(
        id=id,
        title=fake.sentence(nb_words=3),
        author=fake.name(),
        description=fake.sentence(nb_words=10),
        rating=fake.random_int(min=1, max=5),
    )
