from __future__ import annotations
from selenium.webdriver.common.by import By
from .utils import UX, wait_seconds

class SquarespacePage:
    def __init__(self, driver):
        self.d = driver
        self.ux = UX(driver, timeout=12)

    def login(self, email: str, password: str, website: str):
        self.d.get(website)
        self.ux.type(*("name","email"), email)
        self.ux.type(*("name","password"), password)
        self.ux.click(*("xpath","//button[@type='submit']"))
        wait_seconds(2)

    def open_product_inventory(self, url: str):
        self.d.get(url)
        wait_seconds(2)

    # The following methods consolidate duplicated actions.
    def enable_custom_button(self):
        self.ux.click("xpath", "//p[normalize-space()='Custom Button']")
        # fourth checkbox
        boxes = self.d.find_elements(By.XPATH, "//input[@class='css-541w90']")
        if len(boxes) >= 4 and not boxes[3].is_selected():
            boxes[3].click()

    def add_custom_button(self, label: str, url: str):
        self.enable_custom_button()
        # set label and link (placeholders; adjust selectors if needed)
        self.ux.type("xpath", "(//input[@placeholder='Button Text'])[last()]", label)
        self.ux.type("xpath", "(//input[@placeholder='https://'])[last()]", url)

    def save(self):
        self.ux.click("xpath", "//button[.='Save']")
        wait_seconds(1)
