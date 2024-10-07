from core.decorators import has_user_started, language
from pyrogram import Client, filters
from pyrogram.types import KeyboardButton, ReplyKeyboardMarkup, Message


@Client.on_message(filters.command("start") & filters.private)
@has_user_started
@language
async def start(client: Client, message: Message, strings):
    await message.reply_text(
        strings["start_1"].format(message.from_user.mention),
        reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton(strings["button_5"])],
                [
                    KeyboardButton(strings["button_2"]),
                    KeyboardButton(strings["button_3"]),
                ],
                [
                    KeyboardButton(strings["button_6"]),
                    KeyboardButton(strings["button_4"]),
                ],
            ],
            resize_keyboard=True,
        ),
    )
