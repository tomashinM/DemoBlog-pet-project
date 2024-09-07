import os

from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
from redis import Redis
from telebot import TeleBot

from api import API

redis_client = Redis.from_url("redis://redis:6379/2")
api = API(ApiClient(Configuration(host="http://django:8000/api")))
bot = TeleBot(os.environ.get("TELEGRAM_TOKEN"))
