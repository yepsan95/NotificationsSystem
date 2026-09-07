import factory
from faker import Factory as FakerFactory
from pwdlib import PasswordHash
from src.models.user_model import User

password_context = PasswordHash.recommended()

faker = FakerFactory.create()


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None

    first_name = factory.LazyAttribute(lambda _: faker.first_name())
    last_name = factory.LazyAttribute(lambda _: faker.last_name())
    email = factory.LazyAttribute(lambda _: faker.email())
    password_hash = factory.LazyAttribute(
        lambda _: password_context.hash(faker.password())
    )

    middle_name = factory.Maybe(
        factory.LazyAttribute(lambda _: faker.random_int(min=1, max=100) <= 40),
        yes_declaration=factory.LazyAttribute(lambda _: faker.first_name()),
        no_declaration=None,
    )
