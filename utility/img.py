import io
from typing import Tuple

import requests
from PIL import Image, ImageDraw, ImageFilter, ImageChops

from configuration.secret import IMGUR, UNSPLASH


def open_img(path: str) -> Image:
    return Image.open(path)


def upload_img(path: str) -> str:
    return IMGUR.upload_image(path).link


def draw_text(
    img: Image,
    position: Tuple[int, int],
    text: str,
    font: str,
    color: Tuple[int, int, int],
    shadow_color: Tuple[int, int, int],
) -> Image:
    x, y = position
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).text((x + 1, y + 1), text, font=font, fill=shadow_color)
    blurred_shadow = shadow.filter(ImageFilter.BLUR)

    ImageDraw.Draw(blurred_shadow).text(position, text, font=font, fill=color)
    return Image.composite(img, blurred_shadow, ImageChops.invert(blurred_shadow))


def save_img(img: Image, path: str):
    return img.save(path)


def search_unsplash(topic: str, index: int) -> str:
    index = max(1, index)
    photo = UNSPLASH.search.photos(topic, per_page=1, page=index)["results"][0]
    return photo.urls.regular


def dl_img(url: str) -> Image:
    return Image.open(io.BytesIO(requests.get(url).content))


def is_img_file(file: str) -> bool:
    f = file.lower()
    return any(f.endswith(f".{suffix}") for suffix in ["jpg", "jpeg", "gif", "png"])
