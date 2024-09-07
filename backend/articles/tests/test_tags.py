from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from users.tests.mixins import TestMixin
from utils.factories import ArticleFactory, TagFactory


class TestTagViewSet(TestMixin, APITestCase):
    url = reverse_lazy("tags-list")

    def setUp(self):
        super().setUp()
        for i in range(20):
            tag = TagFactory.create(name=str(i))
            # Create i articles with tag i
            for _ in range(i):
                article = ArticleFactory.create()
                article.tags.add(tag)

    def test_get_tags(self):
        # Act
        response = self.client.get(self.url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["tags"]), 10)
        # Tags are ordered by popularity (number of articles)
        self.assertEqual(
            response.data["tags"],
            [str(i) for i in range(19, 9, -1)],
        )
