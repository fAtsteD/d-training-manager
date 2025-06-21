from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler.api_gateway import Router
from aws_lambda_powertools.metrics import MetricUnit

from d_training_manager.telegram import bot

metrics = Metrics(service="webhook-telegram")
router = Router()
tracer = Tracer()
logger = Logger(child=True)


@router.post("/")
@tracer.capture_method
def webhook_telegram() -> tuple:
    metrics.add_metric(name="WebhookTelegramInvocations", unit=MetricUnit.Count, value=1)
    router.current_event.body
    logger.info(f"Telegram Webhook Event received")

    try:
        bot.process_update_dict(router.current_event.json_body)
    except Exception as error:
        logger.error(f"Error processing Telegram webhook", exc_info=error)
        metrics.add_metric(name="WebhookTelegramErrors", unit=MetricUnit.Count, value=1)

    return None, 201
