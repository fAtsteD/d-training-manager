from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.metrics import MetricUnit

metrics = Metrics(service="webhook-telegram")
router = Router()
tracer = Tracer()
logger = Logger(child=True)


@router.post("/")
@tracer.capture_method
def webhook_telegram():
    metrics.add_metric(name="WebhookTelegramInvocations", unit=MetricUnit.Count, value=1)

    logger.info("Telegram Webhook Event")
    return None, 201
