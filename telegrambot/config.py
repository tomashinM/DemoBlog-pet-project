import os

from api import API
from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
from redis import Redis
from telebot import TeleBot

redis_client = Redis.from_url("redis://redis:6379/2")
api = API(ApiClient(Configuration(host="http://django:8000")))
bot = TeleBot(os.environ.get("TELEGRAM_TOKEN"))
