from utility.constant import RESOURCE_PATH, FONT_NAME

import subprocess


def get_resource_path(path: str) -> str:
    return f"{RESOURCE_PATH}/{path}"


def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())


FONT_PATH = get_resource_path(FONT_NAME)
