import logging
from typing import Optional

import requests

from configuration.secret import DARK_SKY_API_KEY
from feature.base import Feature
from utility.html_builder import html_emphasis


class Weather(Feature):

    def __init__(self, latitude: float, longitude: float, city_name: str,
                 div_style: str = "", title: Optional[str] = "今日天气"):
        super().__init__(div_style, title)
        self.latitude = latitude
        self.longitude = longitude
        self.location_name = city_name

    def generate_content(self) -> str:
        data_url = f"https://api.darksky.net/forecast/{DARK_SKY_API_KEY}/{self.latitude},{self.longitude}?lang=zh&units=si"
        data = requests.get(data_url).json()
        logging.info(
                f"Weather: latitude: {data['latitude']}, longitude: {data['longitude']}")
        weather = data["daily"]["data"][0]

        summary = weather["summary"]
        if any(w in summary for w in ["雨", "雪"]):
            summary = html_emphasis(summary)

        min_temperature = int(weather['temperatureLow'])
        min_temperature_text = f"最低 {min_temperature}°C"
        if min_temperature <= 0:
            min_temperature_text = html_emphasis(min_temperature_text)

        return f"{self.location_name} - {summary} 最高 {int(weather['temperatureHigh'])}°C, {min_temperature_text}。"
