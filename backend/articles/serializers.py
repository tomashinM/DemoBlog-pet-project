from django.utils.text import slugify
from rest_framework import serializers
from taggit.serializers import TaggitSerializer, TagListSerializerField

from articles.models import Article, Comment
from users.serializers import ProfileSerializer


class ArticleSerializer(TaggitSerializer, serializers.ModelSerializer):
    tagList = TagListSerializerField(source="tags")
    author = ProfileSerializer(read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)
    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If updating, set the fields to not required
        if self.instance is not None:
            self.fields["title"].required = False
            self.fields["description"].required = False
            self.fields["body"].required = False
            self.fields["tagList"].required = False

    def get_favorited(self, instance) -> bool:
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return instance.favored_by.filter(pk=user.pk).exists()

    def get_favoritesCount(self, instance) -> int:
        return instance.favored_by.count()

    def validate(self, attrs):
        queryset = (
            Article.objects.exclude(pk=self.instance.pk)
            if self.instance
            else Article.objects.all()
        )
        if queryset.filter(slug=slugify(attrs["title"])).exists():
            raise serializers.ValidationError(
                {"slug": "article with this slug already exists."}
            )
        return attrs

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        article = Article(
            author=self.context["request"].user, **validated_data
        )
        article.save()
        article.tags.add(*tags)
        return article

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags")
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        instance.tags.clear()
        instance.tags.add(*tags)

        return instance

    class Meta:
        model = Article
        fields = [
            "title",
            "slug",
            "description",
            "body",
            "tagList",
            "author",
            "createdAt",
            "updatedAt",
            "favorited",
            "favoritesCount",
        ]
        read_only_fields = ["slug"]


class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    createdAt = serializers.DateTimeField(source="created_at", read_only=True)
    updatedAt = serializers.DateTimeField(source="updated_at", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "body", "author", "createdAt", "updatedAt"]
        read_only_fields = ["id"]


class TagSerializer(serializers.Serializer):
    tags = serializers.ListField(child=serializers.CharField())
