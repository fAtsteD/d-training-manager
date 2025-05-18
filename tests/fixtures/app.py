import json
from dataclasses import dataclass
from urllib.parse import urlencode

import faker
import pytest

from d_training_manager import app


@dataclass
class LambdaContext:
    aws_request_id: str
    invoked_function_arn: str = "arn:aws:lambda:us-east-1:123456789012:function:d-training-manager-test-lambda"
    function_name: str = "d-training-manager-test-lambda"
    memory_limit_in_mb: int = 128


@dataclass
class TestResponse:
    status_code: int
    body: dict | None = None
    cookies: list[str] | None = None
    headers: dict | None = None


class HttpApiTestClient:
    """Cliend for request to the lambda function"""

    def __init__(self, lambda_context: LambdaContext, request_id: str, stage: str):
        self.lambda_context = lambda_context
        self.request_id = request_id
        self.stage = stage

    def get(
        self,
        path: str,
        cookies: list[str] = [],
        headers: dict = {},
        params: dict = {},
    ) -> TestResponse:
        return self.request(
            cookies=cookies,
            headers=headers,
            method="GET",
            params=params,
            path=path,
        )

    def post(
        self,
        path: str,
        cookies: list[str] = [],
        data: dict | None = None,
        headers: dict = {},
        params: dict = {},
    ) -> TestResponse:
        return self.request(
            cookies=cookies,
            data=data,
            headers=headers,
            method="POST",
            params=params,
            path=path,
        )

    def put(
        self,
        path: str,
        cookies: list[str] = [],
        data: dict | None = None,
        headers: dict = {},
        params: dict = {},
    ) -> TestResponse:
        return self.request(
            cookies=cookies,
            data=data,
            headers=headers,
            method="PUT",
            params=params,
            path=path,
        )

    def request(
        self,
        path: str,
        cookies: list[str] = [],
        data: dict | None = None,
        headers: dict = {},
        method: str = "GET",
        params: dict = {},
    ) -> TestResponse:
        path = path.lstrip("/")
        params_str = "?" + urlencode(params) if params else ""
        body = json.dumps(data) if data else None
        event = {
            "cookies": cookies,
            "headers": headers,
            "rawPath": f"/{self.stage}/{path}{params_str}",
            "requestContext": {
                "requestContext": {"requestId": self.request_id},
                "http": {
                    "method": method.upper(),
                    "path": f"/{self.stage}/{path}",
                },
                "stage": self.stage,
            },
        }

        if body:
            event["body"] = body

        response = app.lambda_handler(
            context=self.lambda_context,
            event=event,
        )
        return TestResponse(
            body=json.loads(response["body"]),
            cookies=response.get("cookies", []),
            headers=response.get("headers", {}),
            status_code=int(response["statusCode"]),
        )


@pytest.fixture
def http_api_client(
    lambda_context: LambdaContext,
    faker: faker.Faker,
    stage: str,
) -> HttpApiTestClient:
    return HttpApiTestClient(
        lambda_context=lambda_context,
        request_id=str(faker.uuid4()),
        stage=stage,
    )


@pytest.fixture
def lambda_context(faker: faker.Faker) -> LambdaContext:
    return LambdaContext(
        aws_request_id=str(faker.uuid4()),
    )
