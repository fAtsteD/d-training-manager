import os

import pytest
from moto import mock_aws

pytest_plugins = [
    "tests.fixtures.app",
    "tests.fixtures.telegram",
]


@pytest.fixture(autouse=True)
def mocked_aws():
    """
    Mock all AWS interactions
    """
    with mock_aws():
        yield


@pytest.fixture
def stage():
    return os.getenv("STAGE", "test")
