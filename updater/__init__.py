import logging
import sys

logger = logging.getLogger("updater")
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
logHandler = logging.StreamHandler(sys.stdout)
logHandler.setFormatter(logFormatter)
logger.setLevel(logging.INFO)
logger.addHandler(logHandler)
logger.info("Starting updater...")
