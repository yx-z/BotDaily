from utility.constant import RESOURCE_PATH, FONT_NAME


def get_resource(path: str) -> str:
    return f"{RESOURCE_PATH}/{path}"


FONT_PATH = get_resource(FONT_NAME)
