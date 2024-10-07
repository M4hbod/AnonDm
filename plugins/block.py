import os

import aiofiles
from core.database import mongo
from core.decorators import language
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message,
)


def get_unblock_button(self_random_id, strings) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=strings["button_3"], callback_data=f"unblock:{self_random_id}"
                ),
            ],
        ]
    )
    return keyboard


def get_block_button(self_random_id, strings) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=strings["button_2"], callback_data=f"block:{self_random_id}"
                ),
            ],
        ]
    )
    return keyboard


@Client.on_callback_query(filters.regex("^block:"))
@language
async def block_query_handler(client: Client, callback_query: CallbackQuery, strings):
    random_id = callback_query.data.split(":")[1]
    if await mongo.is_blocked(callback_query.from_user.id, random_id):
        return await callback_query.answer(strings["already_blocked"])
    await mongo.block_user(callback_query.from_user.id, random_id)
    await callback_query.message.edit(
        strings["user_blocked"].format(random_id),
        reply_markup=get_unblock_button(random_id, strings),
    )


@Client.on_callback_query(filters.regex("^unblock:"))
@language
async def unblock_query_handler(client: Client, callback_query: CallbackQuery, strings):
    random_id = callback_query.data.split(":")[1]
    if not await mongo.is_blocked(callback_query.from_user.id, random_id):
        return await callback_query.answer(strings["user_not_blocked"])
    await mongo.unblock_user(callback_query.from_user.id, random_id)
    await callback_query.message.edit(
        strings["user_unblocked"].format(random_id),
        reply_markup=get_block_button(random_id, strings),
    )


@Client.on_message(filters.regex(r"^(❌\|مسدود کردن|❌\|Block)$") & filters.private)
@language
async def block_message_handler(client: Client, message: Message, strings):
    random_id = (await client.ask(message.chat.id, strings["send_anon_id"])).text
    if not await mongo.is_user_exist(random_id):
        return await message.reply(strings["user_doesnt_exist"])

    if await mongo.is_blocked(message.from_user.id, random_id):
        return await message.reply(
            strings["user_already_blocked"],
            reply_markup=get_unblock_button(random_id, strings),
        )

    if random_id == await mongo.get_random_id(message.from_user.id):
        return await message.reply(strings["cant_block_self"])

    await mongo.block_user(message.from_user.id, random_id)
    await message.reply(
        strings["user_blocked"].format(random_id),
        reply_markup=get_unblock_button(random_id, strings),
    )


@Client.on_message(filters.regex(r"^(✅\|رفع مسدودیت|✅\|Unblock)$") & filters.private)
@language
async def unblock_message_handler(client: Client, message: Message, strings):
    random_id = (await client.ask(message.chat.id, strings["send_anon_id"])).text
    if not await mongo.is_user_exist(random_id):
        return await message.reply(strings["user_doesnt_exist"])

    if not await mongo.is_blocked(message.from_user.id, random_id):
        return await message.reply(
            strings["user_not_blocked"],
            reply_markup=get_block_button(random_id, strings),
        )

    if random_id == await mongo.get_random_id(message.from_user.id):
        return await message.reply(strings["cant_unblock_self"])

    await mongo.unblock_user(message.from_user.id, random_id)
    await message.reply(
        strings["user_unblocked"].format(random_id),
        reply_markup=get_block_button(random_id, strings),
    )


@Client.on_callback_query(filters.regex("^get_all_blocked$"))
@language
async def get_all_blocked_query_handler(
    client: Client, callback_query: CallbackQuery, strings
):
    blocked = await mongo.get_blocked(callback_query.from_user.id)
    if not blocked:
        return await callback_query.answer(strings["no_blocked_users"])
    block_text = strings["blocked_users"]
    if len("".join(blocked)) > 4096:
        for user in blocked:
            block_text += f"{user}\n"
        async with aiofiles.open(
            f"./blocked-{await mongo.get_random_id(callback_query.from_user.id)}.txt",
            "w",
        ) as file:
            await file.write(block_text)

        await callback_query.message.reply_document(
            f"./blocked-{await mongo.get_random_id(callback_query.from_user.id)}.txt",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=strings["button_7"], callback_data="unblock_all"
                        )
                    ]
                ]
            ),
        )

        os.remove(
            f"./blocked-{await mongo.get_random_id(callback_query.from_user.id)}.txt"
        )

    else:
        for user in blocked:
            block_text += f"`{user}`\n"
        await callback_query.message.edit(
            block_text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=strings["button_7"], callback_data="unblock_all"
                        )
                    ]
                ]
            ),
        )


@Client.on_callback_query(filters.regex("^unblock_all$"))
@language
async def unblock_all_query_handler(
    client: Client, callback_query: CallbackQuery, strings
):
    blocked = await mongo.get_blocked(callback_query.from_user.id)
    if not blocked:
        return await callback_query.answer(strings["no_blocked_users"])
    for user in blocked:
        await mongo.unblock_user(callback_query.from_user.id, user)
    await callback_query.message.edit(strings["all_unblocked"])
