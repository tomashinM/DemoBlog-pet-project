from random import randint, sample

import factory
from django.core.management.base import BaseCommand

from utils.factories import (
    ArticleFactory,
    CommentFactory,
    TagFactory,
    UserFactory,
)


class Command(BaseCommand):
    help = "Populate the database with test data using Factory Boy"

    def add_arguments(self, parser):
        parser.add_argument(
            "--articles",
            type=int,
            default=10,
            help="Number of articles to create",
        )
        parser.add_argument(
            "--users",
            type=int,
            default=5,
            help="Number of users to create",
        )
        parser.add_argument(
            "--tags",
            type=int,
            default=5,
            help="Number of tags to create",
        )
        parser.add_argument(
            "--comments",
            type=int,
            default=5,
            help="Number of comments to create",
        )

    def handle(self, *args, **options):
        users = UserFactory.create_batch(options["users"])
        for user in users:
            excluded = [u for u in users if u != user]
            user.following.add(*sample(excluded, randint(0, len(excluded))))
            user.save()

        tags = TagFactory.create_batch(options["tags"])

        articles = ArticleFactory.create_batch(options["articles"])
        for article in articles:
            CommentFactory.create_batch(
                options["comments"],
                article=article,
                author=factory.Iterator(users),
            )
            article.tags.add(*sample(tags, randint(0, len(tags))))
            article.favored_by.add(*sample(users, randint(0, len(users))))
            article.save()

        self.stdout.write(
            self.style.SUCCESS("Database populated successfully")
        )
