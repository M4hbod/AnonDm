from core.database import mongo
from core.decorators import language
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(
    filters.regex("^(📁\|Profile|📁\|پروفایل)$") & filters.private
)
@language
async def profile_message_handler(_, message, strings):
    blocked = await mongo.get_blocked(message.from_user.id)
    self_random_id = await mongo.get_random_id(message.from_user.id)
    bot = await _.get_me()
    if message.from_user.photo:
        res = await _.get_profile_photos(message.from_user.id, limit=1)
        x = await message.reply_photo(
            res[0].file_id,
            caption=strings["profile"].format(
                message.from_user.id,
                self_random_id,
                bot.username,
                self_random_id,
                len(blocked),
                await mongo.get_join_date(message.from_user.id),
                strings["name"],
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=strings["button_7"],
                            callback_data="unblock_all"
                        ),
                        InlineKeyboardButton(
                            text=strings["button_8"],
                            callback_data="get_all_blocked"
                        ),
                    ]
                ]
            ) if blocked else None,
        )
    else:
        await message.reply_text(
            caption=strings["profile"].format(
                message.from_user.id,
                self_random_id,
                bot.username,
                self_random_id,
                len(blocked),
                await mongo.get_join_date(message.from_user.id),
                strings["name"],
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=strings["button_7"],
                            callback_data="unblock_all"
                        ),
                        InlineKeyboardButton(
                            text=strings["button_8"],
                            callback_data="get_all_blocked"
                        ),
                    ]
                ]
            ) if blocked else None,
        )
