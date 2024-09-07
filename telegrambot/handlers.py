import json

from telebot import types

from config import api, bot, redis_client
from utils import escape_template, send_or_edit


def callback_router(call):
    try:
        data = call.data
        if data.startswith("redis"):
            data = redis_client.get(data)
            if data is None:
                bot.answer_callback_query(call.id, "Sorry, this button has expired.")
                return

        callback_type, data = json.loads(data)
        if callback_type in callback_handlers:
            callback_handlers[callback_type](call, data)
        else:
            bot.answer_callback_query(call.id, "Unknown callback type")
    except (ValueError, TypeError):
        bot.answer_callback_query(call.id, "Invalid callback data")


def handle_article(callback, data):
    slug, params = data
    article = api.articles.articles_retrieve(slug).article
    comments = api.articles.articles_comments_list(slug).comments
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(
            text="⬅️ Back",
            callback_data=json.dumps(("nav", params)),
        ),
        types.InlineKeyboardButton(
            text=f"👤 {article.author.username}",
            callback_data=json.dumps(("author", article.author.username)),
        ),
    )
    text = escape_template(
        "__*$title*__\n\n`$body`\n_$tags _\n\n👤 $author\n📅 _$date _",
        title=article.title,
        body=article.body,
        tags="🏷, ".join(article.tag_list) + "🏷",
        author=article.author.username,
        date=article.created_at.strftime("%Y-%m-%d %H:%M"),
    )
    if comments:
        text += "\n\n__*Comments:*__\n\n||"
        for comment in comments:
            text += escape_template(
                "👤 $author:\n_$comment _\n📅 _$date _\n\n",
                author=comment.author.username,
                date=comment.created_at.strftime("%Y-%m-%d %H:%M"),
                comment=comment.body,
            )
        text += "||"
    else:
        text += "\n\n*No comments yet*"
    send_or_edit(callback.message, text, markup)


def handle_author(callback, data: str):
    articles(callback.message, author=data)


def handle_tag(callback, data: str):
    articles(callback.message, tag=data)


def handle_navigation(callback, data):
    articles(callback.message, **data)


callback_handlers = {
    "article": handle_article,
    "author": handle_author,
    "tag": handle_tag,
    "nav": handle_navigation,
}


def articles(message, **kwargs):
    offset = kwargs.setdefault("offset", 0)
    limit = kwargs.setdefault("limit", 5)

    try:
        if kwargs.get("search"):
            articles = api.search.search_list(**kwargs)
        else:
            articles = api.articles.articles_list(**kwargs)
    except Exception:
        raise AttributeError

    markup = types.InlineKeyboardMarkup()
    for article in articles.articles:
        markup.add(
            types.InlineKeyboardButton(
                text=f"{article.title} by {article.author.username} ❤️({article.favorites_count})",
                callback_data=json.dumps(("article", (article.slug, kwargs))),
            )
        )

    nav_buttons = []
    if offset > 0:
        kwargs["offset"] = offset - limit
        nav_buttons.append(
            types.InlineKeyboardButton(
                "⬅️ Previous",
                callback_data=json.dumps(("nav", kwargs)),
            )
        )
    if limit + offset < articles.articles_count:
        kwargs["offset"] = offset + limit
        nav_buttons.append(
            types.InlineKeyboardButton(
                "Next ➡️",
                callback_data=json.dumps(("nav", kwargs)),
            )
        )
    if nav_buttons:
        markup.row(*nav_buttons)

    params = [key for key in kwargs.keys() if key not in ["offset", "limit"]]
    if params:
        key = params[0]
        if key == "tag":
            title = escape_template("Articles with tag _*$tag*_🏷", tag=kwargs[key])
        elif key == "author":
            profile = api.profiles.profiles_retrieve(kwargs[key]).profile
            title = escape_template(
                "👤 *$author*\nEmail: ||$email||\n\n`$bio`",
                author=profile.username,
                bio=profile.bio,
                email=profile.email,
            )
        elif key == "search":
            title = "🔍 Search results"
        else:
            title = ""
    else:
        title = "Last Articles"

    if articles.articles_count == 0:
        title += "\n\n🤷‍♂️there are no articles🤷‍♂️"

    send_or_edit(message, title, markup)
