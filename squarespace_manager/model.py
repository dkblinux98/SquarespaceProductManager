from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Product:
    title: str
    sku: str
    author: str | None = None
    sneak_peek_url: str | None = None
    amazon_url: str | None = None
    bella_url: str | None = None
