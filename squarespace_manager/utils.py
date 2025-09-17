from __future__ import annotations
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_seconds(n: float) -> None:
    sleep(n)

class UX:
    def __init__(self, driver, timeout: float = 10):
        self.d = driver
        self.timeout = timeout

    def click(self, by, value):
        WebDriverWait(self.d, self.timeout).until(EC.element_to_be_clickable((by, value))).click()

    def type(self, by, value, text: str, clear=True):
        el = WebDriverWait(self.d, self.timeout).until(EC.visibility_of_element_located((by, value)))
        if clear:
            el.clear()
        el.send_keys(text)

    def exists(self, by, value) -> bool:
        try:
            WebDriverWait(self.d, 2).until(EC.presence_of_element_located((by, value)))
            return True
        except:
            return False
