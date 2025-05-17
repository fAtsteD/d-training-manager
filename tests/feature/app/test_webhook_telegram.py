import os

import faker

from d_training_manager import app
from tests.conftest import LambdaContext


def test_access_webhook_telegram(
    faker: faker.Faker,
    lambda_context: LambdaContext,
    stage: str,
):
    """
    Test the access to the telegram webhook
    """
    print(os.getenv("POWERTOOLS_METRICS_NAMESPACE"))
    response = app.lambda_handler(
        context=lambda_context,
        event={
            "rawPath": f"/{stage}/webhook/telegram",
            "requestContext": {
                "requestContext": {"requestId": str(faker.uuid4())},
                "http": {
                    "method": "POST",
                },
                "stage": stage,
            },
        },
    )
    assert response["statusCode"] == 201
