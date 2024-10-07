from config import OWNER_ID
from core.database import mongo
from core.decorators import has_user_started, language
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)


def get_reply_button(self_random_id, strings):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=strings["button_1"], callback_data=f"reply:{self_random_id}"
                ),
                InlineKeyboardButton(
                    text=strings["button_2"], callback_data=f"block:{self_random_id}"
                ),
            ],
        ]
    )
    return keyboard


@Client.on_message(filters.regex("^/start ") & filters.private)
@has_user_started
@language
async def start_send_handler(client: Client, message: Message, strings):
    action, random_id = message.text.split(" ")[1].split("_")
    if action != "dm":
        return

    if not await mongo.is_user_exist(random_id):
        return await message.reply(strings["user_doesnt_exist"])

    self_random_id = await mongo.get_random_id(message.from_user.id)

    target_user_id = await mongo.get_user_id(random_id)
    if await mongo.is_blocked(target_user_id, self_random_id):
        return await message.reply(strings["user_blocked_you"])

    if self_random_id == random_id:
        return await message.reply(
            strings["cant_send_to_yourself"].format(await mongo.get_random_id(OWNER_ID))
        )

    message = await client.ask(
        message.chat.id, strings["send_message"].format(random_id)
    )

    await message.copy(chat_id=target_user_id)
    await client.send_message(
        target_user_id,
        strings["new_message"].format(self_random_id),
        reply_markup=get_reply_button(self_random_id, strings),
    )
    await message.reply(strings["message_sent"].format(random_id))


@Client.on_callback_query(filters.regex("^reply:"))
@language
async def reply_handler(client: Client, callback_query: CallbackQuery, strings):
    random_id = callback_query.data.split(":")[1]
    self_random_id = await mongo.get_random_id(callback_query.from_user.id)
    target_user_id = await mongo.get_user_id(random_id)
    if await mongo.is_blocked(target_user_id, self_random_id):
        return await callback_query.answer(strings["user_blocked_you"])
    await callback_query.message.edit(strings["send_reply"].format(random_id))
    message = await client.listen(callback_query.message.chat.id)
    await message.copy(chat_id=target_user_id)
    await client.send_message(
        target_user_id,
        strings["new_message"].format(self_random_id),
        reply_markup=get_reply_button(self_random_id, strings),
    )
    await message.reply(strings["reply_sent"].format(random_id))


@Client.on_message(
    filters.private & filters.regex(r"^(✉️\|Send Message|✉️\|ارسال پیام)$")
)
@language
async def send_message_handler(client: Client, message: Message, strings):
    random_id = (await client.ask(message.chat.id, strings["send_anon_id"])).text
    if not await mongo.is_user_exist(random_id):
        return await message.reply(strings["user_doesnt_exist"])

    self_random_id = await mongo.get_random_id(message.from_user.id)
    if random_id == self_random_id:
        return await message.reply(
            strings["cant_send_to_yourself"].format(await mongo.get_random_id(OWNER_ID))
        )

    target_user_id = await mongo.get_user_id(random_id)
    if await mongo.is_blocked(target_user_id, self_random_id):
        return await message.reply(strings["user_blocked_you"])

    message = await client.ask(
        message.chat.id, strings["send_message"].format(random_id)
    )

    await message.copy(chat_id=target_user_id)
    await client.send_message(
        target_user_id,
        strings["new_message"].format(self_random_id),
        reply_markup=get_reply_button(self_random_id, strings),
    )
    await message.reply(strings["message_sent"].format(random_id))
