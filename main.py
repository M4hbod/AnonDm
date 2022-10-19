import asyncio

from pyrogram import idle

from core.client import bot


async def main():
    await bot.start()
    print(">> BOT STARTED")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
