import logging

import requests

from configuration.secret import DARK_SKY_API_KEY
from feature.base import Feature


class Weather(Feature):

    def __init__(self, latitude: float, longitude: float, city_name: str,
                 div_style: str = ""):
        super().__init__(div_style)
        self.latitude = latitude
        self.longitude = longitude
        self.location_name = city_name

    @property
    def title(self):
        return "天气"

    def generate_content(self) -> str:
        data_url = f"https://api.darksky.net/forecast/{DARK_SKY_API_KEY}/{self.latitude},{self.longitude}?lang=zh&units=si"
        data = requests.get(data_url).json()
        logging.info(
                f"Weather latitude: {data['latitude']}, longitude: {data['longitude']}")
        weather = data["daily"]["data"][0]

        summary = weather["summary"]
        if any(w in summary for w in ["雨", "雪"]):
            summary = f"<b><i>{summary}</i></b>"  # bold italic

        min_temperature = int(weather['temperatureLow'])
        min_temperature_text = f"最低 {min_temperature}°C"
        if min_temperature <= 0:
            min_temperature_text = f"<i><b>{min_temperature_text}</b></i>"

        return f"{self.location_name} - {summary} 最高 {weather['temperatureHigh']}°C, {min_temperature_text}。"
