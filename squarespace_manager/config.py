from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path
from configparser import ConfigParser
from dotenv import load_dotenv

CONFIG_INI = Path.home() / ".squarespacemanager" / "config.ini"

@dataclass
class Settings:
    email: str
    password: str
    website: str
    product_url: str
    reviews_blog_url: str

def load_settings() -> Settings:
    load_dotenv()  # .env first
    if CONFIG_INI.exists():
        parser = ConfigParser()
        parser.read(CONFIG_INI)
        sec = parser["Squarespace"]
        return Settings(
            email=sec.get("email", os.getenv("SQS_EMAIL", "")),
            password=sec.get("password", os.getenv("SQS_PASSWORD", "")),
            website=sec.get("website", os.getenv("SQS_WEBSITE", "")),
            product_url=sec.get("product_url", os.getenv("SQS_PRODUCT_URL", "")),
            reviews_blog_url=sec.get("reviews_blog_url", os.getenv("SQS_REVIEWS_BLOG_URL", "")),
        )
    return Settings(
        email=os.getenv("SQS_EMAIL", ""),
        password=os.getenv("SQS_PASSWORD", ""),
        website=os.getenv("SQS_WEBSITE", ""),
        product_url=os.getenv("SQS_PRODUCT_URL", ""),
        reviews_blog_url=os.getenv("SQS_REVIEWS_BLOG_URL", ""),
    )
