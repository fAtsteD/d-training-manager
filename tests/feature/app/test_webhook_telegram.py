from tests.fixtures.app import HttpApiTestClient


def test_access_webhook_telegram(
    http_api_client: HttpApiTestClient,
):
    """
    Test the access to the telegram webhook
    """
    response = http_api_client.post(
        path=f"/webhook/telegram",
    )
    assert response.status_code == 201
