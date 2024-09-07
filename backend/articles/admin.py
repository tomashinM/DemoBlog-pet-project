from django.contrib import admin

from articles.models import Article, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "created_at", "updated_at"]
    search_fields = ["title", "slug"]
    list_filter = ["author", "created_at", "updated_at"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["body", "article", "author", "created_at", "updated_at"]
    list_filter = ["author", "created_at", "updated_at"]
