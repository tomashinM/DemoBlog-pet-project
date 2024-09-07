import uuid
from string import Template

from telebot.formatting import escape_markdown
from telebot.types import InlineKeyboardMarkup, Message
from telebot.util import escape

from config import bot, redis_client


def send_or_edit(message: Message, text: str, markup: InlineKeyboardMarkup = None):
    text = escape(text)

    if markup:
        for row in markup.keyboard:
            for button in row:
                if len(button.callback_data.encode("utf-8")) > 64:
                    key = "redis" + uuid.uuid4().hex
                    redis_client.setex(key, 60, button.callback_data)
                    button.callback_data = key

    if message.from_user.is_bot:
        msg = bot.edit_message_text(
            text, message.chat.id, message.message_id, parse_mode="MarkdownV2"
        )
        bot.edit_message_reply_markup(
            message.chat.id, message.message_id, reply_markup=markup
        )
        return msg
    else:
        return bot.send_message(
            message.chat.id, text, reply_markup=markup, parse_mode="MarkdownV2"
        )


def escape_template(template, **kwargs):
    return Template(template).substitute(
        {k: escape_markdown(v) for k, v in kwargs.items()}
    )
