from loki_logger_handler.loki_logger_handler import LokiLoggerHandler
import logging
import sys
import os

loki_handler = LokiLoggerHandler(
    url=os.getenv("LOKI_URL", "http://localhost:3100/loki/api/v1/push"),
    labels={"application": "Google DNS Updater", "environment": "webpi"},
    label_keys={},
    timeout=10
)

logger = logging.getLogger("google_dns_updater")
logger.setLevel(logging.getLevelName(os.getenv("LOG_LEVEL", "INFO")))
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

loki_handler.setFormatter(logFormatter)
logger.addHandler(loki_handler)

logger.debug("Starting updater...")
