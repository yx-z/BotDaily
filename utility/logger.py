import logging
import os

from configuration.secret import LOG_FILE


def setup_prod_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-10s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=LOG_FILE,
    )
    logging.info(f"PID - {os.getpid()}")

def setup_test_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-9s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

