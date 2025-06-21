from http import HTTPStatus

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext

from d_training_manager import config
from d_training_manager.app import webhook_telegram

tracer = Tracer()
logger = Logger()
metrics = Metrics()
app = APIGatewayHttpResolver(
    enable_validation=True,
    response_validation_error_http_code=HTTPStatus.INTERNAL_SERVER_ERROR,
)
app.include_router(webhook_telegram.router, prefix="/webhook/telegram")

if not config.app.is_production:
    app.enable_swagger(
        path="/swagger",
        title="DTraining Manager API",
    )


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
