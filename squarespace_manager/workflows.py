from __future__ import annotations
import csv
from pathlib import Path
from .config import load_settings
from .driver import make_driver
from .page import SquarespacePage
from .model import Product

def read_products(csv_path: str | Path):
    with open(csv_path, newline='', encoding='utf-8') as fh:
        r = csv.DictReader(fh)
        for row in r:
            yield Product(
                title=row.get("Product Title") or row.get("title") or "",
                sku=row.get("SKU") or row.get("sku") or "",
                author=row.get("Author") or row.get("author"),
                sneak_peek_url=row.get("Sneak Peek") or row.get("sneak_peek_url"),
                amazon_url=row.get("Amazon") or row.get("amazon_url"),
                bella_url=row.get("Bella") or row.get("bella_url"),
            )

def update_from_csv(csv_path: str, headless=False):
    cfg = load_settings()
    d = make_driver(headless=headless)
    page = SquarespacePage(d)
    page.login(cfg.email, cfg.password, cfg.website)
    page.open_product_inventory(cfg.product_url)
    # Implement selection by SKU/title and apply updates.
    for p in read_products(csv_path):
        # TODO: locate product by SKU, open editor, update buttons/fields, etc.
        # Example: add a Sneak Peek custom button if URL present
        if p.sneak_peek_url:
            page.add_custom_button("Sneak Peek", p.sneak_peek_url)
        if p.amazon_url:
            page.add_custom_button("Buy on Amazon", p.amazon_url)
        if p.bella_url:
            page.add_custom_button("Buy on Bella", p.bella_url)
        page.save()
    d.quit()
