import random
import string

from core.database import mongo


async def random_id(length: int) -> str:
    random_id = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(length)
    )
    while await mongo.is_user_exist(random_id):
        random_id = "".join(
            random.choice(string.ascii_lowercase + string.digits) for _ in range(length)
        )

    return random_id
