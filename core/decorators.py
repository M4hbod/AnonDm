from lang import get_string

from core.database import mongo
from core.functions import random_id
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery


def language(func):
    async def wrapper(client: Client, update: Message | CallbackQuery, **kwargs):
        if isinstance(update, CallbackQuery):
            chat_id = update.message.chat.id
        elif isinstance(update, Message):
            chat_id = update.chat.id
        language = await mongo.get_language(chat_id)
        language = get_string(language)
        return await func(client, update, language, **kwargs)

    return wrapper


def has_user_started(func):
    async def wrapper(client: Client, message: Message, **kwargs):
        if not await mongo.is_user_started(message.from_user.id):
            await mongo.add_user(message.from_user.id, await random_id(16))
        return await func(client, message, **kwargs)

    return wrapper
