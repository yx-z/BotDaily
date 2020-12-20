import time
from datetime import datetime, timedelta
from math import ceil

from utility.constant import RESOURCE_PATH, FONT_NAME

import signal
from contextlib import contextmanager

import psutil


def sleep_until_next_minute(now: datetime):
    next_minute = datetime(
        now.year, now.month, now.day, now.hour, now.minute
    ) + timedelta(minutes=1)
    sleep_time = max(0, ceil((next_minute - datetime.now()).total_seconds()))
    time.sleep(sleep_time)


def clear_file(file_path: str):
    open(file_path, "w").close()


def get_res_path(path: str) -> str:
    return f"{RESOURCE_PATH}/{path}"


FONT_PATH = get_res_path(FONT_NAME)


def process_exists(process_name: str):
    return process_name in (p.name() for p in psutil.process_iter())


@contextmanager
def timeout_limit(second: int):
    signal.signal(signal.SIGALRM, raise_timeout)
    signal.alarm(second)

    try:
        yield
    except TimeoutError as error:
        raise error
    finally:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum: int, frame: str):
    raise TimeoutError
