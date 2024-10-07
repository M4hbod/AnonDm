import datetime

from config import DEFAULT_LANGUAGE, MONGO_URI
from motor.motor_asyncio import AsyncIOMotorClient


class Mongo:
    def __init__(self, uri: str, database_name: str):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db
        self.users = self.db.users

    async def add_user(self, user_id: int, random_id: str) -> None:
        await self.users.insert_one(
            {
                "user_id": user_id,
                "random_id": random_id,
                "date": datetime.datetime.now(datetime.timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "language": DEFAULT_LANGUAGE,
                "blocked": [],
            }
        )

    async def delete_user(self, user_id: int) -> None:
        await self.users.delete_one({"user_id": user_id})

    async def get_join_date(self, user_id: int) -> str:
        user = await self.users.find_one({"user_id": user_id})
        return user["date"]

    # Block
    async def block_user(self, user_id: int, random_id: str) -> None:
        await self.users.update_one(
            {"user_id": user_id}, {"$push": {"blocked": random_id}}
        )

    async def unblock_user(self, user_id: int, random_id: str) -> None:
        await self.users.update_one(
            {"user_id": user_id}, {"$pull": {"blocked": random_id}}
        )

    async def get_blocked(self, user_id: int) -> bool:
        user = await self.users.find_one({"user_id": user_id})
        return user["blocked"]

    # Boolean
    async def is_blocked(self, user_id: int, random_id: str) -> bool:
        user = await self.users.find_one({"user_id": user_id})
        return random_id in user["blocked"]

    async def is_user_started(self, user_id: int) -> bool:
        user = await self.users.find_one({"user_id": user_id})
        return bool(user)

    async def is_user_exist(self, random_id: str) -> bool:
        user = await self.users.find_one({"random_id": random_id})
        return bool(user)

    # Get ID
    async def get_random_id(self, user_id: int) -> str:
        user = await self.users.find_one({"user_id": user_id})
        return user["random_id"]

    async def get_user_id(self, random_id: str) -> int:
        user = await self.users.find_one({"random_id": random_id})
        return user["user_id"]

    # Language
    async def set_language(self, user_id: int, language: str) -> None:
        await self.users.update_one(
            {"user_id": user_id}, {"$set": {"language": language}}
        )

    async def get_language(self, user_id: int) -> str:
        user = await self.users.find_one({"user_id": user_id})
        return user["language"]


# Database
mongo = Mongo(MONGO_URI, "AnonDm")
