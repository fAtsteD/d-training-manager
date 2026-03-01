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

    id = factory.faker.Faker("random_int", min=1, max=10000)
    first_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    phone = factory.faker.Faker("phone_number")
