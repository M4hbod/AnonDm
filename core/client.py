import pyroaddon
from config import API_HASH, API_ID, BOT_TOKEN
from pyrogram import Client

bot = Client(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

with bot:
    BOT_USERNAME = bot.get_me().username
