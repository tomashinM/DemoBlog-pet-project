import os
import random
import uuid
from functools import wraps
from time import sleep

import django
from locust import HttpUser, between, task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from articles.models import Article  # noqa: E402
from users.models import User  # noqa: E402

USERS = list(User.objects.values_list("email", "username"))
ARTICLES = list(Article.objects.values_list("slug", flat=True))


def authentication_check(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_authenticated:
            return func(self, *args, **kwargs)

    return wrapper


class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.is_authenticated = False
        try:
            self.user = USERS.pop()
        except IndexError:
            print("Add more test users in db")
            self.interrupt()
        response = self.client.post(
            "/api/users/login",
            json={
                "user": {
                    "email": self.user[0],
                    "password": "password123",
                }
            },
        )
        if response.status_code != 200:
            print(f"Failed to log in user {self.user}")
        else:
            self.is_authenticated = True
            self.client.headers["Authorization"] = (
                f"Token {response.json()['user']['token']}"
            )

    def on_stop(self):
        if self.is_authenticated:
            USERS.append(self.user)

    @task(3)
    def view_articles(self):
        self.client.get("/api/articles")

    @task(2)
    @authentication_check
    def view_feed(self):
        self.client.get("/api/articles/feed")

    @task(1)
    def view_article(self):
        slug = random.choice(ARTICLES)
        self.client.get(f"/api/articles/{slug}")
        self.client.get(f"/api/articles/{slug}/comments")

    @task(1)
    @authentication_check
    def create_comment(self):
        slug = random.choice(ARTICLES)
        response = self.client.post(
            f"/api/articles/{slug}/comments",
            json={"comment": {"body": "This is a test comment"}},
        )
        sleep(1)
        self.client.delete(
            f"/api/articles/{slug}/comments/{response.json()['comment']['id']}"
        )

    @task(1)
    @authentication_check
    def favorite_article(self):
        slug = random.choice(ARTICLES)
        self.client.post(f"/api/articles/{slug}/favorite")
        if random.choice([True, False]):
            self.client.delete(f"/api/articles/{slug}/favorite")

    @task(1)
    @authentication_check
    def crud_article(self):
        response = self.client.post(
            "/api/articles",
            json={
                "article": {
                    "title": str(uuid.uuid4()),
                    "description": "This is a test",
                    "body": "This is a test",
                    "tagList": ["test"],
                }
            },
        )
        slug = response.json()["article"]["slug"]
        self.client.get(f"/api/articles/{slug}")
        self.client.delete(f"/api/articles/{slug}")

    @task(1)
    def search_articles(self):
        query = random.choice(random.choice(ARTICLES).split("-"))
        self.client.get(f"/api/search?search={query}")

    @task(2)
    @authentication_check
    def view_profile(self):
        self.client.get(f"/api/profiles/{self.user[1]}")

    @task(1)
    @authentication_check
    def follow_user(self):
        _, username = random.choice(USERS)
        self.client.post(f"/api/profiles/{username}/follow")
        sleep(1)
        if random.choice([True, False]):
            self.client.delete(f"/api/profiles/{username}/follow")
