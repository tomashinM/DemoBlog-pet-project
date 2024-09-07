from django.db import connection, models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django_prometheus.models import ExportModelOperationsMixin
from taggit.managers import TaggableManager

from utils.tasks import send_new_article_notification


class Article(ExportModelOperationsMixin("article"), models.Model):
    """
    Article model
    """

    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(
        max_length=120, allow_unicode=True, blank=True, db_index=True
    )
    description = models.CharField(max_length=255)
    body = models.TextField()
    tags = TaggableManager(blank=True, related_name="articles")
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="articles"
    )
    favored_by = models.ManyToManyField(
        "users.User", related_name="favorite_articles", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Article)
def article_pre_save(sender, instance, **kwargs):
    instance.slug = slugify(instance.title, allow_unicode=True)


@receiver(post_save, sender=Article)
def article_post_save(sender, instance, created, **kwargs):
    if created and "test" not in connection.settings_dict["NAME"]:
        recipients = [
            user.email
            for user in instance.author.followers.filter(notifications=True)
        ]
        if recipients:
            send_new_article_notification.delay(recipients, instance.slug)


class Comment(ExportModelOperationsMixin("comment"), models.Model):
    """
    Comment model
    """

    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="comments"
    )
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body
