from django.db.models import Count
from django_filters import rest_framework as filters

from articles.models import Article


class CustomOrderingFilter(filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra["choices"] += [
            ("favoritesCount", "likes"),
            ("-favoritesCount", "likes_desc"),
        ]

    def filter(self, qs, value):
        if not value:
            return qs

        if any(v in ["favoritesCount", "-favoritesCount"] for v in value):
            return qs.annotate(favoritesCount=Count("favored_by")).order_by(
                *value
            )

        return super().filter(qs, value)


class ArticleFilter(filters.FilterSet):
    tag = filters.CharFilter(field_name="tags__name")
    author = filters.CharFilter(field_name="author__username")
    favorited = filters.CharFilter(field_name="favored_by__username")
    ordering = CustomOrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        )
    )

    class Meta:
        model = Article
        fields = ["author", "tag", "favorited"]
