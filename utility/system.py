from utility.constant import RESOURCE_PATH, FONT_NAME

import psutil


def get_resource_path(path: str) -> str:
    return f"{RESOURCE_PATH}/{path}"


FONT_PATH = get_resource_path(FONT_NAME)


def process_exists(process_name):
    return process_name in (p.name() for p in psutil.process_iter())
