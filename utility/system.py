from utility.constant import RESOURCE_PATH, FONT_NAME

import signal
from contextlib import contextmanager

import psutil


def clear_file(file_path: str):
    open(file_path, "w").close()


def get_resource_path(path: str) -> str:
    return f"{RESOURCE_PATH}/{path}"


FONT_PATH = get_resource_path(FONT_NAME)


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
