import json

from django.test.utils import override_settings
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase
from taggit.models import Tag

from articles.models import Article
from users.tests.mixins import TestMixin
from utils.factories import ArticleFactory


@override_settings(ELASTICSEARCH_DSL_AUTOSYNC=False)
class TestArticleViewSet(TestMixin, APITestCase):
    url = reverse_lazy("articles-list")
    data = {
        "title": "Test Title",
        "description": "Test Description",
        "body": "Test Body",
        "tagList": ["test"],
    }

    def setUp(self):
        super().setUp()
        tag = Tag.objects.create(name="Test Tag")
        self.article = Article.objects.create(
            title="Test Article",
            description="Test Description",
            body="Test Body",
            author=self.celeb_user,
        )
        self.article.tags.add(tag)

    def test_create_article_unauthenticated(self):
        # Act
        response = self.client.post(self.url, {})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_article(self):
        # Arrange
        self.client.force_authenticate(user=self.celeb_user)

        # Act
        response = self.client.post(self.url, {"article": self.data})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["article"]["favorited"], False)
        self.assertEqual(response.data["article"]["favoritesCount"], 0)
        author = response.data["article"]["author"]
        self.assertEqual(author["username"], self.celeb_user.username)
        self.assertEqual(author["bio"], self.celeb_user.bio)
        self.assertEqual(author["image"], self.celeb_user.image)
        self.assertEqual(author["following"], False)

        self.assertEqual(self.celeb_user.articles.count(), 2)
        article = self.celeb_user.articles.filter(slug="test-title").first()
        self.assertIsNotNone(article)
        self.assertEqual(article.title, self.data["title"])
        self.assertEqual(article.description, self.data["description"])
        self.assertEqual(article.body, self.data["body"])
        tags = list(article.tags.all().values_list("name", flat=True))
        self.assertEqual(tags, self.data["tagList"])

        return article

    def test_create_article_with_existing_slug(self):
        # Arrange
        data = self.data.copy()
        data["title"] = "Test Article"
        self.client.force_authenticate(user=self.celeb_user)

        # Act
        response = self.client.post(self.url, {"article": data})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["errors"]["title"][0],
            "article with this title already exists.",
        )

    def test_get_article(self):
        # Arrange
        url = reverse_lazy(
            "articles-detail", kwargs={"slug": self.article.slug}
        )

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in [
            "title",
            "description",
            "body",
            "tagList",
            "author",
            "createdAt",
            "updatedAt",
            "favorited",
            "favoritesCount",
        ]:
            self.assertIsNotNone(response.data["article"].get(key))

    def test_update_article(self):
        # Arrange
        new_data = {
            "title": "New Title",
            "description": "New Description",
            "body": "New Body",
            "tagList": ["new"],
        }
        url = reverse_lazy(
            "articles-detail", kwargs={"slug": self.article.slug}
        )
        self.client.force_authenticate(user=self.celeb_user)

        # Act
        response = self.client.put(url, {"article": new_data})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, new_data["title"])
        self.assertEqual(self.article.slug, "new-title")
        self.assertEqual(self.article.description, new_data["description"])
        self.assertEqual(self.article.body, new_data["body"])
        tags = list(self.article.tags.all().values_list("name", flat=True))
        self.assertEqual(tags, new_data["tagList"])

    def test_update_article_not_owned(self):
        # Arrange
        url = reverse_lazy(
            "articles-detail", kwargs={"slug": self.article.slug}
        )
        self.client.force_authenticate(user=self.user)

        # Act
        response = self.client.put(url, {})

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_article(self):
        # Arrange
        url = reverse_lazy(
            "articles-detail", kwargs={"slug": self.article.slug}
        )
        self.client.force_authenticate(user=self.celeb_user)

        # Act
        response = self.client.delete(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.celeb_user.articles.count(), 0)
        self.assertFalse(
            Article.objects.filter(slug=self.article.slug).exists()
        )

    def test_delete_article_not_owned(self):
        # Arrange
        url = reverse_lazy(
            "articles-detail", kwargs={"slug": self.article.slug}
        )
        self.client.force_authenticate(user=self.user)

        # Act
        response = self.client.delete(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.celeb_user.articles.count(), 1)
        self.assertTrue(
            Article.objects.filter(slug=self.article.slug).exists()
        )

    def test_list_articles(self):
        # Arrange
        ArticleFactory.create_batch(99)

        # Act
        response = self.client.get(self.url)
        data = json.loads(response.content)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["articles"]), 20)
        self.assertEqual(data["articlesCount"], 100)

    def test_list_articles_with_limit(self):
        # Arrange
        ArticleFactory.create_batch(99)

        # Act
        response = self.client.get(self.url + "?limit=50")
        data = json.loads(response.content)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["articles"]), 50)
        self.assertEqual(data["articlesCount"], 100)

    def test_list_articles_with_filters(self):
        # Arrange
        Tag.objects.create(name="A")
        Tag.objects.create(name="B")
        for _ in range(5):
            article = ArticleFactory.create(author=self.celeb_user)
            article.tags.add("A")
        for _ in range(10):
            article = ArticleFactory.create(author=self.user)
            article.tags.add("B")

        for article in Article.objects.all()[:3]:
            article.favored_by.add(self.user)

        # Filter by tag
        response = self.client.get(self.url + "?tag=A")
        self.assertEqual(json.loads(response.content)["articlesCount"], 5)
        # Filter by author
        response = self.client.get(self.url + f"?author={self.user.username}")
        self.assertEqual(json.loads(response.content)["articlesCount"], 10)
        # Filter by favorited
        response = self.client.get(
            self.url + f"?favorited={self.user.username}"
        )
        self.assertEqual(json.loads(response.content)["articlesCount"], 3)

    def test_get_feed_unauthenticated(self):
        # Act
        response = self.client.get(reverse_lazy("articles-feed"))

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_feed(self):
        # Arrange
        self.celeb_user.followers.add(self.user)
        ArticleFactory.create_batch(5, author=self.celeb_user)
        ArticleFactory.create_batch(5, author=self.user)
        self.client.force_authenticate(user=self.user)

        # Act
        response = self.client.get(reverse_lazy("articles-feed"))
        data = json.loads(response.content)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["articlesCount"], 6)
        for article in data["articles"]:
            self.assertEqual(
                article["author"]["username"], self.celeb_user.username
            )

    def test_favorite_unauthenticated(self):
        # Act
        response = self.client.post(
            reverse_lazy("articles-favorite", kwargs={"slug": "test-article"})
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_favorite_article(self):
        # Arrange
        url = reverse_lazy(
            "articles-favorite", kwargs={"slug": self.article.slug}
        )
        self.client.force_authenticate(user=self.user)

        # Act: Favorite
        response = self.client.post(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.article.favored_by.filter(pk=self.user.pk).exists()
        )
        self.assertEqual(response.data["article"]["favorited"], True)
        self.assertEqual(response.data["article"]["favoritesCount"], 1)

        # Act: Un-favorite
        response = self.client.delete(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            self.article.favored_by.filter(pk=self.user.pk).exists()
        )
        self.assertEqual(response.data["article"]["favorited"], False)
        self.assertEqual(response.data["article"]["favoritesCount"], 0)

    def test_list_articles_with_ordering(self):
        # Arrange
        ArticleFactory.create().favored_by.set(
            [self.admin_user, self.user, self.celeb_user]
        )
        ArticleFactory.create().favored_by.set([self.admin_user])
        ArticleFactory.create().favored_by.set([self.admin_user, self.user])

        # Act
        response = self.client.get(self.url + "?ordering=favoritesCount")
        data = json.loads(response.content)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [x["favoritesCount"] for x in data["articles"]], [0, 1, 2, 3]
        )
