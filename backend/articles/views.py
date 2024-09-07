from django.db.models import Count
from django_elasticsearch_dsl.search import Search
from django_elasticsearch_dsl_drf.filter_backends import (
    CompoundSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from taggit.models import Tag

from articles.documents import ArticleDocument
from articles.filters import ArticleFilter
from articles.models import Article, Comment
from articles.paginations import ArticlePagination
from articles.serializers import (
    ArticleSerializer,
    CommentSerializer,
    TagSerializer,
)
from utils.parsers import get_custom_parser
from utils.wrappers import ErrorSerializer, wrap_response, wrap_schema


class ArticleViewSet(ModelViewSet):
    """
    API endpoints for articles
    """

    object_name = "article"
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filterset_class = ArticleFilter
    http_method_names = ["get", "post", "put", "delete"]
    parser_classes = [get_custom_parser(object_name)]

    @wrap_response(object_name)
    @wrap_schema(object_name)(serializer_class, serializer_class, 201)
    def create(self, request, *args, **kwargs):
        """
        Create article
        """
        return super().create(request, *args, **kwargs)

    @wrap_response(object_name)
    @wrap_schema(object_name)(
        response_serializer=serializer_class, error_statuses=[400]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Get an article
        """
        return super().retrieve(request, *args, **kwargs)

    @wrap_response(object_name)
    @wrap_schema(object_name)(serializer_class, serializer_class)
    def update(self, request, *args, **kwargs):
        """
        Update an article
        """
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Article.objects.none()
        queryset = (
            Article.objects.select_related("author")
            .prefetch_related("tags", "favored_by")
            .order_by("-created_at")
        )
        if self.action in ["update", "destroy"]:
            return queryset.filter(author=self.request.user)
        if self.action == "feed":
            return queryset.filter(author__followers=self.request.user)
        return queryset

    def get_permissions(self):
        if self.request.method not in SAFE_METHODS or self.action == "feed":
            return [IsAuthenticated()]
        return []

    @extend_schema(
        responses={
            "200": serializer_class(many=True),
            "400": ErrorSerializer,
            "401": ErrorSerializer,
        }
    )
    @action(detail=False)
    def feed(self, request, *args, **kwargs):
        """
        Articles feed
        """
        return self.list(self, request, *args, **kwargs)

    @wrap_response(object_name)
    @wrap_schema(object_name)(response_serializer=serializer_class)
    @action(detail=True, methods=["POST", "DELETE"])
    def favorite(self, request, *args, **kwargs):
        """
        Like/Unlike an article
        """
        article = self.get_object()

        if request.method == "POST":
            article.favored_by.add(request.user)
        elif request.method == "DELETE":
            article.favored_by.remove(request.user)

        return Response(self.get_serializer(article).data)


class ArticleSearchView(BaseDocumentViewSet):
    document = ArticleDocument
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    serializer_class = ArticleSerializer
    pagination_class = ArticlePagination
    filter_backends = [CompoundSearchFilterBackend]
    search_fields = {
        "title": {"boost": 4},
        "description": {"boost": 2},
        "body": None,
    }

    # Use Search class from django_elastisearch_dsl to get to_queryset() method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search = Search(
            using=self.client,
            index=self.index,
            doc_type=self.document._doc_type.name,
            model=self.document.Django.model,
        )

    @extend_schema(parameters=[OpenApiParameter("search")])
    def list(self, request, *args, **kwargs):
        """
        Search for articles
        """
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.to_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagView(APIView):
    @extend_schema(
        responses={
            "200": TagSerializer,
            "400": ErrorSerializer,
        }
    )
    def get(self, request, *args, **kwargs):
        """
        List of most popular tags
        """
        tags = list(
            Tag.objects.all()
            .values("name")
            .annotate(count=Count("articles"))
            .order_by("-count")[:10]
            .values_list("name", flat=True)
        )
        serializer = TagSerializer({"tags": tags})
        return Response(serializer.data)


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    API endpoints for comments
    """

    object_name = "comment"
    serializer_class = CommentSerializer
    parser_classes = [get_custom_parser(object_name)]

    @wrap_response(object_name)
    @wrap_schema(object_name)(serializer_class, serializer_class, 201)
    def create(self, request, *args, **kwargs):
        """
        Create new comment for an article
        """
        return super().create(request, *args, **kwargs)

    @wrap_response(object_name + "s")
    @wrap_schema(object_name + "s", many=True)(
        response_serializer=serializer_class
    )
    def list(self, request, *args, **kwargs):
        """
        List comments for an article
        """
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Comment.objects.none()
        queryset = (
            Comment.objects.select_related("author")
            .filter(article__slug=self.kwargs["slug"])
            .order_by("-created_at")
        )
        if self.action == "destroy":
            return queryset.filter(author=self.request.user)
        return queryset

    def perform_create(self, serializer):
        article = Article.objects.get(slug=self.kwargs["slug"])
        serializer.save(author=self.request.user, article=article)
