from lang import get_string

from core.database import mongo
from core.functions import random_id


def language(func):

    async def wrapper(_, update, **kwargs):
        try:
            language = await mongo.get_language(update.chat.id)
        except AttributeError:
            language = await mongo.get_language(update.message.chat.id)
        language = get_string(language)
        return await func(_, update, language, **kwargs)

    return wrapper


def is_user_started(func):

    async def wrapper(_, message, **kwargs):
        if not await mongo.is_user_started(message.from_user.id):
            await mongo.add_user(message.from_user.id, await random_id(16))
        return await func(_, message, **kwargs)

    return wrapper
