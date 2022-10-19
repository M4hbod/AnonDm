import pyroaddon
from config import API_HASH, API_ID, BOT_TOKEN
from pyrogram import Client

proxy = {"scheme": "socks5", "hostname": "127.0.0.1", "port": 10808}

bot = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins"),
    proxy=proxy,
)

with bot:
    BOT_USERNAME = bot.get_me().username
