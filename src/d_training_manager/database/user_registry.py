import time
from uuid import uuid4

from pynamodb.exceptions import DoesNotExist

from d_training_manager.database.models import DBUser


class UserRegistry:
    pass


def get_by_id(user_id: str) -> DBUser | None:
    try:
        return DBUser.get(user_id, consistent_read=True)
    except DoesNotExist:
        pass

    return None


def get_by_phone(phone: str) -> DBUser | None:
    result = DBUser.phone_index.query(phone, limit=1)
    return next(result, None)


def get_by_telegram_id(telegram_id: int) -> DBUser | None:
    result = DBUser.telegram_index.query(telegram_id, limit=1)
    return next(result, None)


def update(user: DBUser):
    if not user.id:
        user.id = str(uuid4())

    if not user.created_at:
        user.created_at = int(time.time())

    user.updated_at = int(time.time())
    user.save()
