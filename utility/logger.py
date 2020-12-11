import logging
import os

from configuration.secret import LOG_FILE

from utility.constant import DATE_FORMAT, TIME_FORMAT


def setup_prod_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-10s %(message)s",
        datefmt=f"{DATE_FORMAT} {TIME_FORMAT}",
        filename=LOG_FILE,
    )
    logging.info(f"PID - {os.getpid()}")


def setup_test_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-9s %(message)s",
        datefmt=f"{DATE_FORMAT} {TIME_FORMAT}",
    )
