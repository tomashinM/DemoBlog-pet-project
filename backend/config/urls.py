from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from articles.views import (
    ArticleSearchView,
    ArticleViewSet,
    CommentViewSet,
    TagView,
)
from users.views import ProfileViewSet, UserView, UserViewSet

router = DefaultRouter(trailing_slash=False)
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")
router.register("articles", ArticleViewSet, basename="articles")
router.register("search", ArticleSearchView, basename="articles-search")
commentsRouter = DefaultRouter(trailing_slash=False)
commentsRouter.register(
    "comments", CommentViewSet, basename="article-comments"
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/", include(router.urls)),
    re_path(r"^api/articles/(?P<slug>[\w-]+)/", include(commentsRouter.urls)),
    path("api/user", UserView.as_view(), name="user"),
    path("api/tags", TagView.as_view(), name="tags-list"),
    path("", include("django_prometheus.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
