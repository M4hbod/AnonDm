from core.database import mongo
from core.decorators import language
from lang import get_string, languages_present
from pykeyboard import InlineKeyboard
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup,
    Message,
    CallbackQuery,
)


def lanuages_keyboard(_) -> InlineKeyboard:
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            (
                InlineKeyboardButton(
                    text=languages_present[i],
                    callback_data=f"languages:{i}",
                )
            )
            for i in languages_present
        ]
    )
    return keyboard


@Client.on_message(filters.regex(r"^(🏳️\|Language|🏳️\|زبان)$") & filters.private)
@language
async def language(client: Client, message: Message, strings):
    keyboard = lanuages_keyboard(strings)
    await message.reply_text(strings["lang_1"], reply_markup=keyboard)


@Client.on_callback_query(filters.regex(r"languages:(.*?)"))
async def language_markup(client: Client, callback_query: CallbackQuery):
    langauge = (callback_query.data).split(":")[1]
    old = await mongo.get_language(callback_query.message.chat.id)
    if str(old) == str(langauge):
        strings = get_string(old)
        return await callback_query.answer(strings["lang_2"], show_alert=True)
    try:
        strings = get_string(langauge)
        await callback_query.message.reply(
            strings["lang_3"],
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
        await callback_query.message.delete()
    except:
        return await callback_query.answer(
            strings["lang_4"],
            show_alert=True,
        )
    await mongo.set_language(callback_query.message.chat.id, langauge)
