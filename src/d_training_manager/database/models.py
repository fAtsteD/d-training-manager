from pynamodb.attributes import NumberAttribute, UnicodeAttribute
from pynamodb.indexes import AllProjection, GlobalSecondaryIndex
from pynamodb.models import Model

from d_training_manager import config

_database_host = config.database.url


class DBBaseModel(Model):
    class Meta:  # pyright: ignore
        host = _database_host
        read_capacity_units = 1
        write_capacity_units = 1


class DBUser(Model):

    class Meta:  # pyright: ignore
        table_name = f"d-training-manager-{config.app.stage.value.lower()}-users"
        host = _database_host
        read_capacity_units = 1
        write_capacity_units = 1

    class DBIndexUserPhone(GlobalSecondaryIndex):

        class Meta:  # pyright: ignore
            index_name = f"users-phone-index"
            read_capacity_units = 1
            write_capacity_units = 1
            projection = AllProjection()

        phone = UnicodeAttribute(hash_key=True)

    class DBIndexUserTelegram(GlobalSecondaryIndex):

        class Meta:  # pyright: ignore
            index_name = f"users-telegram-index"
            read_capacity_units = 1
            write_capacity_units = 1
            projection = AllProjection()

        telegram_id = NumberAttribute(hash_key=True)
        phone = UnicodeAttribute(range_key=True)

    created_at = NumberAttribute(null=False)
    id = UnicodeAttribute(hash_key=True, null=False)
    first_name = UnicodeAttribute(null=False)
    last_name = UnicodeAttribute(null=False)
    phone = UnicodeAttribute()
    phone_index = DBIndexUserPhone()
    telegram_id = NumberAttribute()
    telegram_index = DBIndexUserTelegram()
    updated_at = NumberAttribute(null=False)
