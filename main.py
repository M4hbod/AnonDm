import asyncio

from pyrogram import idle

from core.client import BOT_USERNAME, bot


async def main():
    await bot.start()
    print(f">> BOT STARTED @{BOT_USERNAME}")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
