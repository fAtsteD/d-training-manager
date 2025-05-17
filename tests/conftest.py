from dataclasses import dataclass

import faker
import pytest
from moto import mock_aws


@dataclass
class LambdaContext:
    aws_request_id: str
    invoked_function_arn: str = "arn:aws:lambda:us-east-1:123456789012:function:d-training-manager-test-lambda"
    function_name: str = "d-training-manager-test-lambda"
    memory_limit_in_mb: int = 128


@pytest.fixture
def lambda_context(faker: faker.Faker) -> LambdaContext:
    return LambdaContext(
        aws_request_id=str(faker.uuid4()),
    )


@pytest.fixture(scope="function")
def mocked_aws():
    """
    Mock all AWS interactions
    """
    with mock_aws():
        yield
