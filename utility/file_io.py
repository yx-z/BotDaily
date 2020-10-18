from utility.constant import RESOURCE_PATH, FONT_NAME


def get_resource_path(path: str) -> str:
    return f"{RESOURCE_PATH}/{path}"


FONT_PATH = get_resource_path(FONT_NAME)
