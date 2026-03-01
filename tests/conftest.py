import os

import pytest
from moto import mock_aws

from d_training_manager.database.models import DBUser

pytest_plugins = [
    "tests.fixtures.app",
    "tests.fixtures.telegram",
]


@pytest.fixture(autouse=True)
def mocked_aws():
    with mock_aws():
        yield


@pytest.fixture(autouse=True)
def database_tables(mocked_aws):
    if DBUser.exists():
        DBUser.delete_table()

    DBUser.create_table(wait=True)
    yield
    DBUser.delete_table()


@pytest.fixture
def stage():
    return os.getenv("STAGE", "test")
