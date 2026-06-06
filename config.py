from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Обязательная переменная окружения не задана: {key}")
    return value


@dataclass
class Config:
    FigmaFileKey: str
    FigmaToken: str
    
    def __init__(self):
        self.FigmaFileKey = _require("FIGMA_FILE_KEY")
        self.FigmaToken = _require("FIGMA_TOKEN")
        
app_config = Config()