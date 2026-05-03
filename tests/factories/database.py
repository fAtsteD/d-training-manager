from typing import TypeVar

import factory

from d_training_manager.database.models import DBBaseModel, DBUser

FactoryModelType = TypeVar("FactoryModelType", bound=DBBaseModel)


class BaseFactory[FactoryModelType](factory.base.Factory[FactoryModelType]):

    class Meta:  # pyright: ignore
        abstract = True

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return model_class(*args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        instance = model_class(*args, **kwargs)
        instance.save()
        return instance


class DBUserFactory(BaseFactory[DBUser]):
    class Meta:  # pyright: ignore
        model = DBUser

    created_at = factory.faker.Faker("unix_time")
    id = factory.faker.Faker("uuid4")
    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    phone = factory.faker.Faker("phone_number")
    telegram_id = factory.faker.Faker("random_int", min=1, max=1000000)
    updated_at = factory.faker.Faker("unix_time")
