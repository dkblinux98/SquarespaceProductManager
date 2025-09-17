from __future__ import annotations
import argparse
from .config import load_settings
from .driver import make_driver
from .page import SquarespacePage
from .workflows import update_from_csv

def main():
    ap = argparse.ArgumentParser(prog="sqsp")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_login = sub.add_parser("login")
    ap_login.add_argument("--headless", action="store_true")

    ap_update = sub.add_parser("update")
    ap_update.add_argument("--csv", required=True)
    ap_update.add_argument("--headless", action="store_true")

    args = ap.parse_args()
    if args.cmd == "login":
        cfg = load_settings()
        d = make_driver(headless=args.headless)
        page = SquarespacePage(d)
        page.login(cfg.email, cfg.password, cfg.website)
        page.open_product_inventory(cfg.product_url)
        print("Logged in.")
        d.quit()
    elif args.cmd == "update":
        update_from_csv(args.csv, headless=args.headless)
