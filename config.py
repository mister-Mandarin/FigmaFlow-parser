from dataclasses import dataclass

import streamlit as st


def _require(key: str) -> str:
    # Локально — из .streamlit/secrets.toml, в облаке — из Streamlit Secrets
    value = st.secrets.get(key)
    if not value:
        raise EnvironmentError(f"Обязательная переменная окружения не задана: {key}")
    return value


@dataclass
class Config:
    AppEnv: str
    FigmaToken: str
    FigmaFileKey: str = ""

    def __init__(self):
        self.FigmaToken = _require("FIGMA_TOKEN")
        self.AppEnv = _require("APP_ENV")

    def parse_link_url(self, url: str) -> bool:
        parts = url.split("/")
        if len(parts) < 5 or parts[3] != "design":
            raise ValueError("Некорректный URL Figma")
        self.FigmaFileKey = parts[4]
        return True


app_config = Config()
