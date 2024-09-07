import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import connection, models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django_prometheus.models import ExportModelOperationsMixin

from utils.tasks import send_verification_email


class CustomUserManager(UserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        # Set is_active to True for superusers
        extra_fields.setdefault("is_active", True)
        return super().create_superuser(
            username, email, password, **extra_fields
        )


class User(ExportModelOperationsMixin("user"), AbstractUser):
    """
    User model
    """

    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True, null=True)
    following = models.ManyToManyField(
        "self", related_name="followers", symmetrical=False
    )
    verification_token = models.UUIDField(default=uuid.uuid4, null=True)
    is_active = models.BooleanField(default=False)
    notifications = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @cached_property
    def token(self) -> str:
        from rest_framework_simplejwt.tokens import RefreshToken

        return str(RefreshToken.for_user(self).access_token)

    def is_following(self, user: "User") -> bool:
        return self.following.filter(pk=user.pk).exists()


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created and "test" not in connection.settings_dict["NAME"]:
        send_verification_email.delay(instance.id)
