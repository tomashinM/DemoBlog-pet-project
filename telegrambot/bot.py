import json
import re

from telebot import types

from config import api, bot
from handlers import articles, callback_router
from utils import send_or_edit


@bot.message_handler(commands=["start"])
def start_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("/articles", "/popular_tags", "/search")
    bot.send_message(
        message.chat.id, "⭐️Welcome to DemoBlog in Telegram⭐️", reply_markup=markup
    )


@bot.message_handler(commands=["articles"])
def articles_command(message):
    articles(message)


@bot.message_handler(commands=["popular_tags"])
def tags_command(message):
    tags = api.tags.tags_retrieve().tags
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for tag in tags:
        buttons.append(
            types.InlineKeyboardButton(text=tag, callback_data=json.dumps(("tag", tag)))
        )
    markup.row(*buttons)
    send_or_edit(
        message,
        f"Popular tags 🏷{'\nthere are no tags' if not tags else ''}",
        markup,
    )


@bot.message_handler(commands=["search"])
def search_command(message):
    msg = send_or_edit(message, "🔍 Введите поисковой запрос:")
    bot.register_next_step_handler(msg, handle_search_reply)


def handle_search_reply(message):
    articles(message, search=re.sub(r"[^a-zA-Z0-9\s\-_]", "", message.text)[:30])


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    callback_router(call)


bot.polling(non_stop=True)
