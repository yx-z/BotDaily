import logging
from datetime import datetime
from pathlib import Path

from configuration.secret import LOG_DIR

from utility.constant import DATE_FORMAT, TIME_FORMAT

LOG_FORMAT = "%(asctime)s %(levelname)-10s %(message)s"


def setup_prod_logger(date: datetime):
    Path.mkdir(Path(LOG_DIR), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=f"{DATE_FORMAT} {TIME_FORMAT}",
        filename=f"{LOG_DIR}/prod_{date.strftime('%Y%m%d')}.log",
    )


def setup_test_logger(date: datetime):
    Path.mkdir(Path(LOG_DIR), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=f"{DATE_FORMAT} {TIME_FORMAT}",
        handlers=[
            logging.FileHandler(
                f"{LOG_DIR}/test_{date.strftime('%Y%m%d')}.log"),
            logging.StreamHandler(),
        ],
    )
