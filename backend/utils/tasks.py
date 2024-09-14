import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = get_task_logger(__name__)


class EmailSender:
    def __init__(self, subject, html_template, params):
        self.subject = subject
        self.html_template = html_template
        self.params = params

    def send(self, recipients):
        html = render_to_string(self.html_template, self.params)
        send_mail(
            self.subject,
            strip_tags(html),
            os.environ.get("SUPERUSER_EMAIL"),
            recipients,
            html_message=html,
        )


@shared_task
def send_verification_email(user_id):
    from users.models import User

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error("User does not exist")
        return
    email = EmailSender(
        "Verify your email address",
        "email_verification.html",
        {
            "user": user,
            "token": str(user.verification_token),
            "hostname": os.environ.get("SITE_URL"),
        },
    )
    email.send([user.email])


@shared_task
def send_new_article_notification(recipient_list, slug):
    from articles.models import Article

    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        logger.error("Article does not exist")
        return
    email = EmailSender(
        f"{article.author.username} posted new article {article.title}",
        "new_article_notification.html",
        {"article": article, "hostname": os.environ.get("SITE_URL")},
    )
    email.send(recipient_list)
