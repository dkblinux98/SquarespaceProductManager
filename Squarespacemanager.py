import csv
import time
import datetime
import os
import configparser

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Get the current time
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%H:%M:%S")


# Utility Functions

def wait_seconds(seconds_to_wait):
    time.sleep(seconds_to_wait)


# Main class
class SquarespaceManager:
    def __init__(self):
        self.password = None
        self.email = None
        self.website = None
        self.product_url = None
        self.reviews_blog_url = None
        self.driver = None
        self.config_path = os.path.expanduser("~/.squarespacemanager/config.ini")
        self.product_title = None
        self.product_sku = None
        self.product_author = None
        self.product_peek = None
        self.product_amazon = None
        self.product_bella = None
        self.page_editorial_review = None
        self.driver = None

    def init_driver(self):
        self.load_config()
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36")
        options.add_experimental_option("detach", True)
        chrome_driver_path = ChromeDriverManager().install()
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

    def load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        self.email = config.get("Credentials", "email")
        self.password = config.get("Credentials", "password")
        self.website = config.get("URLs", "website")
        self.product_url = config.get("URLs", "product_url")
        self.reviews_blog_url = config.get("URLs", "reviews_blog_url")

    def login_squarespace(self):
        self.driver.get(self.website)
        wait_seconds(2)

        # Click Squarespace Log In button on Home Page
        self.driver.find_element(By.CLASS_NAME, "www-navigation__desktop__account-info__login-button").click()
        wait_seconds(2)

        # Input email and password
        self.driver.find_element(By.NAME, "email").send_keys(self.email)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        wait_seconds(2)

        # Click login
        self.driver.find_element(By.CLASS_NAME, "css-1cmjwkf").click()
        wait_seconds(5)

    def load_product(self):
        self.driver.get(self.product_url)
        wait_seconds(15)

        # Search by SKU for the next product to update
        self.driver.find_element(By.CLASS_NAME, "css-1ixgjfk").click()
        actions = ActionChains(self.driver)
        actions.send_keys(self.product_sku)
        actions.perform()
        wait_seconds(5)

        # Click on the product for editing
        self.driver.find_element(By.XPATH, "//*[@id=\"inventory-table\"]/tbody/tr[1]/td[3]/div/div/img").click()
        wait_seconds(2)

    def update_custom_button(self):
        # Wait for Custom Button to be clickable and then click it to open up the editor pop-up
        locate = WebDriverWait(self.driver, 5)
        element = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='css-11jecpf' and text()='Custom Button']")))
        element.click()

        # Enable the Custom Button (fourth instance of the class)
        checkboxes = self.driver.find_elements(By.XPATH, "//input[@class='css-541w90']")
        if len(checkboxes) >= 4:
            checkbox = checkboxes[3]
            checkbox.click()

            # Provide the Custom Button Label
            textarea = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[@class='css-1caatvj']")))
            # Use keyboard shortcuts to clear the text
            textarea.send_keys(Keys.COMMAND + 'a')  # Select all text
            textarea.send_keys(Keys.DELETE)  # Delete selected text
            textarea.send_keys("Buy eBook")  # Enter the new text
            wait_seconds(2)

            # Find and click the "Apply" button
            apply_button = self.driver.find_element(By.XPATH, "//button[contains(span, 'Apply')]")
            apply_button.click()
            wait_seconds(2)

    def add_additional_information(self):
        locate = WebDriverWait(self.driver, 10)

        # Open Additional Info for editing
        additional_info = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='css-11jecpf' and text()='Additional Info']")))
        additional_info.click()
        wait_seconds(5)

    def add_books_by_author_summary_block(self):
        locate = WebDriverWait(self.driver, 10)
        # Add a Summary Block for Books by Author

        # Click into the initial text box to activate the plus sign. (Stupid classic editor)
        text_box = self.driver.find_element(By.CLASS_NAME, "rte-placeholder")
        text_box.click()
        wait_seconds(2)

        # Click the plus sign to activate the modal to add a Summary block
        plus_sign = locate.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".insert-point-icon")))
        plus_sign.click()
        wait_seconds(2)

        # Click the Summary block
        book_summary = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='block-selector-button-summary-wall']")))
        book_summary.click()
        wait_seconds(2)

        # Click the Page option to select a page
        select_page = locate.until(EC.element_to_be_clickable((By.XPATH,
                                                               "//p[@class='XkI909ywMpCRUvpID57a TIzi3RduH0Y4vdAS6ZPR undefined css-1jplqdq' and text()='Select a Page']")))
        select_page.click()
        wait_seconds(2)

        # Choose the Shop page
        select_shop = locate.until(EC.element_to_be_clickable((By.XPATH,
                                                               "//p[@class='XkI909ywMpCRUvpID57a TIzi3RduH0Y4vdAS6ZPR undefined css-1jplqdq' and text()='Shop']")))
        select_shop.click()
        wait_seconds(2)

        # Go back to the main modal page
        back_button = locate.until(EC.element_to_be_clickable((By.CLASS_NAME, "css-rn4s5f")))
        back_button.click()
        wait_seconds(2)

        # Select the filter option to set a filter
        select_filter = locate.until(EC.element_to_be_clickable((By.XPATH,
                                                                 "//p[@class='XkI909ywMpCRUvpID57a TIzi3RduH0Y4vdAS6ZPR undefined css-1jplqdq' and text()='Filter Items']")))
        select_filter.click()
        wait_seconds(2)

        # Activate the tags dropdown
        dropdown_tags = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1m4unsj' and text()='Tag']")))
        dropdown_tags.click()
        wait_seconds(5)

        # Select the desired tag filter. Note that this will select only one filter
        # If more than one was needed this would have to be modified
        select_tag_xpath = f"//p[@class='css-11jecpf' and text()='{self.product_author}']"
        select_tag = self.driver.find_element(By.XPATH, select_tag_xpath)
        select_tag.click()
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        wait_seconds(5)

        # Close the modal temporarily to re-enter and get to the Design tab
        # Had to press Escape key to get out of the modal and then click the Summary
        # block again and click Edit to bring the modal back up in order to modify
        # the Design tab. This is why I HATE the classic editor. It is so buggy.

        # Re-select the summary block and click the edit button
        select_summary = locate.until(EC.element_to_be_clickable((By.CLASS_NAME, "sqs-editing-overlay")))
        select_summary.click()
        wait_seconds(5)
        select_edit = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='jbNjFVr_t46zQ423HO_N css-u12dw2']")))
        select_edit.click()

        # Click the Design tab
        edit_design = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='css-92gdcr' and text()='Design']")))
        edit_design.click()
        wait_seconds(2)

        # Choose Carousel and set the desired display options
        # I know this is an ugly and un-discernible sequence of action chains
        # But it works. And trying to find each element via XPATH, etc.
        # would be a nightmare.
        select_carousel = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1jplqdq' and text()='Wall']")))
        select_carousel.click()
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.DOWN)
        actions.send_keys(Keys.ENTER)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys("30")
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys("5")
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.DOWN)
        actions.send_keys(Keys.DOWN)
        actions.send_keys(Keys.DOWN)
        actions.send_keys(Keys.DOWN)
        actions.send_keys(Keys.DOWN)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.key_down(Keys.COMMAND).send_keys('a').key_up(Keys.COMMAND)
        actions.pause(2)
        actions.send_keys(Keys.DELETE)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.SPACE)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.SPACE)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.SPACE)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.SPACE)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        wait_seconds(5)

    def add_author_bio_summary_block(self):
        locate = WebDriverWait(self.driver, 10)

        # Add a Summary Block for Author Bio And, yes, I know there is duplicate code here. The classic editor is so
        # buggy, it's probably a fluke that the same process for finding the elements worked twice.

        # Click into the initial text box to activate the plus sign. (Stupid classic editor)
        text_box = self.driver.find_element(By.CLASS_NAME, "rte-placeholder")
        text_box.click()
        wait_seconds(2)

        # Click the plus sign to activate the modal to add a Summary block. Notice this is a different path
        # from the one used for the books by author block. The previous path wouldn't work this time. {{shrug}}
        # Also calling this from within the for loop, this wouldn't work unless I left the detach mode enabled.
        # Again, {{shrug}}
        plus_sign = self.driver.find_elements(By.CLASS_NAME, "sqs-layout-insert-point-button")
        if len(plus_sign) >= 3:
            third_insert_button = plus_sign[2]
            third_insert_button.click()
        wait_seconds(2)

        # Click the Summary block
        author_summary = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='block-selector-button-summary-wall']")))
        author_summary.click()
        wait_seconds(2)

        # Click the Page option to select a page
        select_page = locate.until(EC.element_to_be_clickable((By.XPATH,
                                                               "//p[@class='XkI909ywMpCRUvpID57a TIzi3RduH0Y4vdAS6ZPR undefined css-1jplqdq' and text()='Select a Page']")))
        select_page.click()
        wait_seconds(2)

        # Choose the Author Bios page
        select_shop = locate.until(EC.element_to_be_clickable((By.XPATH,
                                                               "//p[@class='XkI909ywMpCRUvpID57a TIzi3RduH0Y4vdAS6ZPR undefined css-1jplqdq' and text()='Author Bios']")))
        select_shop.click()
        wait_seconds(2)

        # Go back to the main modal page
        back_button = locate.until(EC.element_to_be_clickable((By.CLASS_NAME, "css-rn4s5f")))
        back_button.click()
        wait_seconds(2)

        # Select the filter option to set a filter
        select_filter = locate.until(EC.element_to_be_clickable((By.XPATH,
                                                                 "//p[@class='XkI909ywMpCRUvpID57a TIzi3RduH0Y4vdAS6ZPR undefined css-1jplqdq' and text()='Filter Items']")))
        select_filter.click()
        wait_seconds(2)

        # Activate the tags dropdown
        dropdown_tags = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1m4unsj' and text()='Tag']")))
        dropdown_tags.click()
        wait_seconds(5)

        # Select the desired tag filter. Note that this will select only one filter
        # If more than one was needed this would have to be modified
        select_tag_xpath = f"//p[@class='css-11jecpf' and text()='{self.product_author}']"
        select_tag = self.driver.find_element(By.XPATH, select_tag_xpath)
        select_tag.click()
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        wait_seconds(5)

        # Close the modal temporarily to re-enter and get to the Design tab
        # Had to press Escape key to get out of the modal and then click the Summary
        # block again and click Edit to bring the modal back up in order to modify
        # the Design tab. This is why I HATE the classic editor. It is so buggy.

        # Re-select the summary block and click the edit button. Notice I had to do this differently this time
        # in order to get it to work. {{shrug}}
        select_summary = self.driver.find_elements(By.CLASS_NAME, "sqs-editing-overlay")
        if len(select_summary) >= 2:
            second_select_button = select_summary[1]
            second_select_button.click()
        wait_seconds(5)
        select_edit = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='jbNjFVr_t46zQ423HO_N css-u12dw2']")))
        select_edit.click()

        # Click the Design tab
        edit_design = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='css-92gdcr' and text()='Design']")))
        edit_design.click()
        wait_seconds(2)

        # Choose List and set the desired display options
        # I know this is an ugly and un-discernible sequence of action chains
        # But it works. And trying to find each element via XPATH, etc.
        # would be a nightmare.
        select_list = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1jplqdq' and text()='Wall']")))
        select_list.click()
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.DOWN)
        actions.send_keys(Keys.DOWN)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys("1")
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.SPACE)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        wait_seconds(5)

    def add_sneak_peek_button(self):

        summary_box = self.driver.find_element(By.CLASS_NAME, "sqs-editing-overlay")
        summary_box.click()
        wait_seconds(2)

        add_button_element = self.driver.find_element(By.XPATH,
                                                      "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/button/span")
        add_button_element.click()
        wait_seconds(5)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.SPACE)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys("Get Sneak Peek")
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(self.product_peek)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        wait_seconds(5)

    def add_buy_amazon_button(self):

        add_button_element = self.driver.find_element(By.XPATH,
                                                      "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/button/span")
        add_button_element.click()
        wait_seconds(5)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.SPACE)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys("Buy on Amazon")
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(self.product_amazon)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        wait_seconds(5)

    def add_buy_bella_button(self):

        add_button_element = self.driver.find_element(By.XPATH,
                                                      "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/button/span")
        add_button_element.click()
        wait_seconds(5)
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.SPACE)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys("Buy on Bella")
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(self.product_bella)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        wait_seconds(5)

    def add_paperbacks_text(self):
        locate = WebDriverWait(self.driver, 10)

        add_text_element = self.driver.find_element(By.XPATH,
                                                    "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/button/span")
        add_text_element.click()
        wait_seconds(5)
        select_textbox = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='css-8c43tr' and text()='Text']")))
        select_textbox.click()
        write_paperbacks = self.driver.find_element(By.XPATH,
                                                    "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div/div/p")
        write_paperbacks.click()
        actions = ActionChains(self.driver)
        actions.send_keys("Paperbacks")
        actions.perform()
        wait_seconds(2)

    def add_books_by_author_text(self):
        locate = WebDriverWait(self.driver, 10)

        add_text_element = self.driver.find_element(By.XPATH,
                                                    "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/button/span")
        add_text_element.click()
        wait_seconds(5)
        select_textbox = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='css-8c43tr' and text()='Text']")))
        select_textbox.click()
        write_books_by_author = self.driver.find_element(By.XPATH,
                                                         "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[2]/div[2]/div/div/p")
        write_books_by_author.click()
        actions = ActionChains(self.driver)
        actions.send_keys("Books By Author")
        actions.perform()
        wait_seconds(2)

    def add_spacers(self):
        locate = WebDriverWait(self.driver, 10)

        add_spacer_element = self.driver.find_element(By.XPATH,
                                                      "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/button/span")
        add_spacer_element.click()
        wait_seconds(5)
        select_spacer = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='css-8c43tr' and text()='Spacer']")))
        select_spacer.click()
        wait_seconds(2)

        add_spacer_element = self.driver.find_element(By.XPATH,
                                                      "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[4]")
        add_spacer_element.click()
        wait_seconds(5)
        select_plus_sign = self.driver.find_element(By.XPATH,
                                                    "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div[1]/button/span")
        select_plus_sign.click()
        wait_seconds(5)
        select_spacer = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='css-8c43tr' and text()='Spacer']")))
        select_spacer.click()
        wait_seconds(2)

    def add_editorial_reviews_summary_block(self):
        # Load DPP Editorial Reviews
        locate = WebDriverWait(self.driver, 15)

        # Click into the summary box for author bios to activate plus sign
        summary_box = self.driver.find_element(By.CLASS_NAME, "sqs-editing-overlay")
        summary_box.click()
        wait_seconds(2)

        # Click the plus sign to add a summary block for editorial reviews
        select_reviews_summary_block = locate.until(
            EC.element_to_be_clickable((By.XPATH, "(//span[@class='insert-point-icon'])[17]")))
        select_reviews_summary_block.click()

        # Add Summary Block
        review_summary = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='block-selector-button-summary-wall']")))
        review_summary.click()
        wait_seconds(2)

        # Click the Page option to select a page
        select_page = locate.until(EC.element_to_be_clickable((By.XPATH,
                                                               "//p[@class='XkI909ywMpCRUvpID57a TIzi3RduH0Y4vdAS6ZPR undefined css-1jplqdq' and text()='Select a Page']")))
        select_page.click()
        wait_seconds(2)

        # Choose the Editorial Reviews page
        select_reviews = locate.until(EC.element_to_be_clickable((By.XPATH,
                                                                  "//p[@class='XkI909ywMpCRUvpID57a TIzi3RduH0Y4vdAS6ZPR undefined css-1jplqdq' and text()='Editorial Reviews']")))
        select_reviews.click()
        wait_seconds(2)

        # Go back to the main modal page
        back_button = locate.until(EC.element_to_be_clickable((By.CLASS_NAME, "css-rn4s5f")))
        back_button.click()
        wait_seconds(2)

        # Update Primary Metadata to None
        date_posted = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='GMKgKC5HljsKQAomuKwi' and text()='Date Posted']")))
        date_posted.click()

        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.pause(2)
        actions.perform()

        # Update Tags
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        wait_seconds(2)

        # Activate the tags dropdown
        dropdown_tags = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1m4unsj' and text()='Tag']")))
        dropdown_tags.click()
        wait_seconds(5)

        # Select the desired tag filter. Note that this will select only one filter
        # If more than one is needed this will have to be modified
        select_tag_xpath = f"//p[@class='css-11jecpf' and text()='{self.product_title}']"
        select_tag = self.driver.find_element(By.XPATH, select_tag_xpath)
        select_tag.click()
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        wait_seconds(5)

        # Go back to the main modal page
        actions = ActionChains(self.driver)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.pause(10)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        wait_seconds(2)

        # Select the Design tab
        design_tab = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='css-92gdcr' and text()='Design']")))
        design_tab.click()

        # Make necessary edits to the Design
        # Choose List and set the desired display options
        # I know this is an ugly and un-discernible sequence of action chains
        # But it works. And trying to find each element via XPATH, etc.
        # would be a nightmare.
        select_list = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1jplqdq' and text()='Wall']")))
        select_list.click()
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.DOWN)
        actions.send_keys(Keys.DOWN)
        actions.send_keys(Keys.ENTER)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys("1")
        actions.perform()
        wait_seconds(2)

        # 14 tabs to uncheck title
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.SPACE)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.SPACE)
        actions.pause(2)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        wait_seconds(2)

    def add_editorial_reviews_text(self):
        # TODO Need to fix this to change text to Header 1 and center justified
        locate = WebDriverWait(self.driver, 10)

        # Click into the summary box for author bios to activate plus sign
        summary_box = self.driver.find_element(By.CLASS_NAME, "sqs-editing-overlay")
        summary_box.click()
        wait_seconds(2)

        # Click the plus sign to add a summary block for editorial reviews
        select_reviews_summary_block = locate.until(
            EC.element_to_be_clickable((By.XPATH, "(//span[@class='insert-point-icon'])[17]")))
        select_reviews_summary_block.click()

        # Select the text box and add the Editorial Review Title
        text_box = locate.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='css-8c43tr' and text()='Text']")))
        text_box.click()
        write_review_title = locate.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='rte-placeholder']")))
        write_review_title.click()
        actions = ActionChains(self.driver)
        actions.send_keys("Editorial Reviews, Awards, and Accolades")
        actions.perform()
        wait_seconds(2)

    def save_work(self):
        apply_button = self.driver.find_element(By.CLASS_NAME, "css-17t69sc")
        apply_button.click()
        wait_seconds(2)
        save_button = self.driver.find_element(By.CLASS_NAME, "css-xrk2u6")
        save_button.click()
        wait_seconds(2)

    def add_editorial_reviews_blog_posts(self):
        self.driver.get(self.reviews_blog_url)
        wait_seconds(15)

        locate = WebDriverWait(self.driver, 10)

        # Click plus to add a new review
        add_review = locate.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[1]/div/div[2]/button")))
        add_review.click()
        wait_seconds(10)

        iframe_id = "sqs-site-frame"
        self.driver.switch_to.frame(iframe_id)

        # Add the Book title as the review title and the review text from the spreadsheet
        add_title = locate.until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[5]/main/article/section/div[2]/div/div/article/div/div[1]/div[1]/h1/span")))
        add_title.click()
        wait_seconds(2)

        actions = ActionChains(self.driver)
        actions.send_keys(self.product_title)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(self.page_editorial_review)
        actions.send_keys(Keys.ESCAPE)
        actions.pause(2)
        actions.perform()
        wait_seconds(2)

        self.driver.switch_to.default_content()

        # Save the new review
        save_review = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='css-lmv9yd' and text()='Save']")))
        save_review.click()
        wait_seconds(20)

        # Search for the newly added review to update the settings
        search_for_review = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@class='R9jw9mDrfU1u0BPCVHFi css-1ixgjfk']")))
        search_for_review.click()
        wait_seconds(10)

        actions = ActionChains(self.driver)
        actions.send_keys(self.product_title)
        actions.pause(10)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.pause(2)
        actions.perform()
        wait_seconds(10)

        # Select Settings from the dropdown
        select_settings = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//li[@class='css-bcz4rq' and text()='Settings']")))
        select_settings.click()
        wait_seconds(2)

        # 11 tabs to get to Excerpt
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(self.page_editorial_review)
        actions.perform()
        wait_seconds(2)

        # 10 tabs to get to Options Menu Item
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        wait_seconds(2)

        # 5 tabs to get to Options Status
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        wait_seconds(2)

        # 4 tabs to Set Published
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.SPACE)
        actions.perform()
        wait_seconds(2)

        # 3 back tabs to click Back
        actions = ActionChains(self.driver)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.perform()
        wait_seconds(2)

        # 10 tabs and a space to Add tags
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(Keys.ENTER)
        actions.pause(2)
        actions.send_keys(self.product_title)
        actions.send_keys(Keys.ENTER)
        actions.pause(2)
        actions.perform()

        # 11 back tabs to get to Save
        actions = ActionChains(self.driver)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.pause(5)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.pause(5)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.pause(5)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        actions.pause(5)
        actions.send_keys(Keys.ENTER)
        actions.pause(15)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()
        wait_seconds(2)

        # Clear search for next review
        clear_search = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='G32HI27XogfDtZnoOuJV ZPafWOAWUD7zvunyYQ0p']")))
        clear_search.click()
        wait_seconds(2)

    def update_sneak_peek(self):
        # Replace Sneak Peek Link with google drive link
        locate = WebDriverWait(self.driver, 15)

        # Click into the Get Sneak Peek button to edit
        peek_button = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='sqs-block-button-container sqs-block-button-container--right']")))
        peek_button.click()
        wait_seconds(2)

        # Click the Edit Button
        edit_peek_button = locate.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='jbNjFVr_t46zQ423HO_N css-u12dw2']")))
        edit_peek_button.click()
        wait_seconds(2)

        # Click into the edit box
        edit_box = locate.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='css-11hgc42' and text()='Content']")))
        edit_box.click()
        wait_seconds(2)

        # Edit the link
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.TAB)
        actions.pause(2)
        actions.send_keys(self.product_peek)
        actions.pause(2)
        actions.send_keys(Keys.ESCAPE)
        actions.perform()

    def update_products_from_csv(self):
        csv_file_path = "/Users/darlabaker/Desktop/dpp-product-list.csv"
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                self.product_sku = row['SKU']
                self.product_title = row['Title']
                self.product_author = row['Author']
                self.product_peek = row['Sneak Peek Link']
                self.product_amazon = row['Amazon Link']
                self.product_bella = row['Bella Link']
                self.page_editorial_review = row['Review']

                # Get the current time
                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")
                print("Current time:", formatted_time)
                print(f"Updating product: {self.product_title}")

                # self.add_editorial_reviews_blog_posts()
                self.load_product()
                self.add_additional_information()
                # self.add_books_by_author_summary_block()
                # self.add_author_bio_summary_block()
                # self.add_sneak_peek_button()
                # self.add_buy_amazon_button()
                # self.add_buy_bella_button()
                # self.add_paperbacks_text()
                # self.add_books_by_author_text()
                # self.add_spacers()
                # self.add_editorial_reviews_summary_block()
                # self.add_editorial_reviews_text()
                # self.update_sneak_peek()
                wait_seconds(45)
                self.save_work()


                current_time = datetime.datetime.now()
                formatted_time = current_time.strftime("%H:%M:%S")
                print("Current time:", formatted_time)
                print(f"Updated product: {self.product_title}")
                wait_seconds(10)


manager = SquarespaceManager()
manager.init_driver()
manager.load_config()
manager.login_squarespace()
# manager.load_product()
manager.update_products_from_csv()
# manager.update_custom_button()
# manager.add_additional_information()
# manager.add_books_by_author_summary_block()
# manager.add_author_bio_summary_block()
# manager.add_sneak_peek_button()
# manager.add_buy_amazon_button()
# manager.add_buy_bella_button()
# manager.add_paperbacks_text()
# manager.add_books_by_author_text()
# manager.add_spacers()
# manager.add_editorial_reviews_summary_block()
# manager.add_editorial_reviews_text()
# manager.save_work()
# manager.add_editorial_reviews_blog_posts()
