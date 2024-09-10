import factory
from faker import Faker
from taggit.models import Tag

from articles.models import Article, Comment
from users.models import User

fake = Faker("ru_RU")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyFunction(fake.user_name)
    email = factory.LazyFunction(fake.email)
    bio = factory.LazyFunction(fake.text)
    is_active = True
    password = factory.PostGenerationMethodCall("set_password", "password123")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = factory.LazyFunction(fake.word)


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.LazyFunction(fake.sentence)
    description = factory.LazyFunction(fake.paragraph[:255])
    body = factory.LazyFunction(fake.text)
    author = factory.SubFactory(UserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    body = factory.LazyFunction(fake.paragraph[:255])
    article = factory.SubFactory(ArticleFactory)
    author = factory.SubFactory(UserFactory)
