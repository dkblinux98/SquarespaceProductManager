import csv
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# Utility Functions

def wait_seconds(seconds_to_wait):
    time.sleep(seconds_to_wait)


# Main class

class SquarespaceManager:
    def __init__(self):
        self.product_title = None
        self.product_sku = None
        self.product_author = None
        self.product_peek = None
        self.product_amazon = None
        self.product_bella = None
        self.driver = None

    def init_driver(self):
        options = Options()
        options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36")
        options.add_experimental_option("detach", True)
        chrome_driver_path = ChromeDriverManager().install()
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.maximize_window()

    def login_squarespace(self):
        self.driver.get("http://www.squarespace.com")
        wait_seconds(2)

        # Click Squarespace Log In button on Home Page
        self.driver.find_element(By.CLASS_NAME, "www-navigation__desktop__account-info__login-button").click()
        wait_seconds(2)

        # Input email and password
        self.driver.find_element(By.NAME, "email").send_keys("<your email address>")
        self.driver.find_element(By.NAME, "password").send_keys("<your password")
        wait_seconds(2)

        # Click login
        self.driver.find_element(By.CLASS_NAME, "css-1cmjwkf").click()
        wait_seconds(5)

        # Load DPP Product -> Service
        self.driver.get("https://desertpalmpress.squarespace.com/config/commerce/products/service")
        wait_seconds(15)

    def load_product(self):
        locate = WebDriverWait(self.driver, 5)

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

            # save_work defined separately. Leaving this here because save_work
            # uses a different path to find the button.
            # # Click Save to return to the Product Inventory Listing
            # save_button = WebDriverWait(self.driver, 5).until(
            #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='pc-save-button']")))
            # save_button.click()

    def add_additional_information(self):
        locate = WebDriverWait(self.driver, 10)

        # Open Additional Info for editing
        additional_info = locate.until(
            EC.element_to_be_clickable((By.XPATH, "//p[@class='css-11jecpf' and text()='Additional Info']")))
        additional_info.click()
        wait_seconds(5)

    def add_books_by_author(self):
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
        book_summary = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='block-selector-button-summary-wall']")))
        book_summary.click()
        wait_seconds(2)

        # Click the Page option to select a page
        select_page = locate.until(EC.element_to_be_clickable((By.XPATH,"//p[@class='dkYlsXI7FUn4IhE3g7Xp irRsiAA4s5zIfInwUF3Z undefined css-1jplqdq' and text()='Select a Page']")))
        select_page.click()
        wait_seconds(2)

        # Choose the Shop page
        select_shop = locate.until(EC.element_to_be_clickable((By.XPATH,"//p[@class='dkYlsXI7FUn4IhE3g7Xp irRsiAA4s5zIfInwUF3Z undefined css-1jplqdq' and text()='Shop']")))
        select_shop.click()
        wait_seconds(2)

        # Go back to the main modal page
        back_button = locate.until(EC.element_to_be_clickable((By.CLASS_NAME, "css-rn4s5f")))
        back_button.click()
        wait_seconds(2)

        # Select the filter option to set a filter
        select_filter = locate.until(EC.element_to_be_clickable((By.XPATH,"//p[@class='dkYlsXI7FUn4IhE3g7Xp irRsiAA4s5zIfInwUF3Z undefined css-1jplqdq' and text()='Filter Items']")))
        select_filter.click()
        wait_seconds(2)

        # Activate the tags dropdown
        dropdown_tags = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1m4unsj' and text()='Tag']")))
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
        select_edit = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='jbNjFVr_t46zQ423HO_N css-u12dw2']")))
        select_edit.click()

        # Click the Design tab
        edit_design = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='css-92gdcr' and text()='Design']")))
        edit_design.click()
        wait_seconds(2)

        # Choose Carousel and set the desired display options
        # I know this is an ugly and un-discernible sequence of action chains
        # But it works. And trying to find each element via XPATH, etc.
        # would be a nightmare.
        select_carousel = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1jplqdq' and text()='Wall']")))
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

    def add_author_bio(self):
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
        author_summary = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='block-selector-button-summary-wall']")))
        author_summary.click()
        wait_seconds(2)

        # Click the Page option to select a page
        select_page = locate.until(EC.element_to_be_clickable((By.XPATH,"//p[@class='dkYlsXI7FUn4IhE3g7Xp irRsiAA4s5zIfInwUF3Z undefined css-1jplqdq' and text()='Select a Page']")))
        select_page.click()
        wait_seconds(2)

        # Choose the Author Bios page
        select_shop = locate.until(EC.element_to_be_clickable((By.XPATH,"//p[@class='dkYlsXI7FUn4IhE3g7Xp irRsiAA4s5zIfInwUF3Z undefined css-1jplqdq' and text()='Author Bios']")))
        select_shop.click()
        wait_seconds(2)

        # Go back to the main modal page
        back_button = locate.until(EC.element_to_be_clickable((By.CLASS_NAME, "css-rn4s5f")))
        back_button.click()
        wait_seconds(2)

        # Select the filter option to set a filter
        select_filter = locate.until(EC.element_to_be_clickable((By.XPATH,"//p[@class='dkYlsXI7FUn4IhE3g7Xp irRsiAA4s5zIfInwUF3Z undefined css-1jplqdq' and text()='Filter Items']")))
        select_filter.click()
        wait_seconds(2)

        # Activate the tags dropdown
        dropdown_tags = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1m4unsj' and text()='Tag']")))
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
        select_edit = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='jbNjFVr_t46zQ423HO_N css-u12dw2']")))
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
        select_list = locate.until(EC.element_to_be_clickable((By.XPATH, "//*[@class='css-1jplqdq' and text()='Wall']")))
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

        add_button_element = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/button/span")
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

        add_button_element = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/button/span")
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

        add_button_element = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/button/span")
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

        add_text_element = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/button/span")
        add_text_element.click()
        wait_seconds(5)
        select_textbox = locate.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='css-8c43tr' and text()='Text']")))
        select_textbox.click()
        write_paperbacks = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div/div/p")
        write_paperbacks.click()
        actions = ActionChains(self.driver)
        actions.send_keys("Paperbacks")
        actions.perform()
        wait_seconds(2)

    def add_books_by_author_text(self):
        locate = WebDriverWait(self.driver, 10)

        add_text_element = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/button/span")
        add_text_element.click()
        wait_seconds(5)
        select_textbox = locate.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='css-8c43tr' and text()='Text']")))
        select_textbox.click()
        write_books_by_author = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[2]/div[2]/div/div/p")
        write_books_by_author.click()
        actions = ActionChains(self.driver)
        actions.send_keys("Books By Author")
        actions.perform()
        wait_seconds(2)

    def add_spacers(self):
        locate = WebDriverWait(self.driver, 10)

        add_spacer_element = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/button/span")
        add_spacer_element.click()
        wait_seconds(5)
        select_spacer = locate.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='css-8c43tr' and text()='Spacer']")))
        select_spacer.click()
        wait_seconds(2)

        add_spacer_element = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[4]")
        add_spacer_element.click()
        wait_seconds(5)
        select_plus_sign = self.driver.find_element(By.XPATH, "/html/body/div[21]/div[2]/div/div[2]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div[1]/button/span")
        select_plus_sign.click()
        wait_seconds(5)
        select_spacer = locate.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='css-8c43tr' and text()='Spacer']")))
        select_spacer.click()
        wait_seconds(2)

    def save_work(self):
        apply_button = self.driver.find_element(By.CLASS_NAME, "css-17t69sc")
        apply_button.click()
        wait_seconds(2)
        save_button = self.driver.find_element(By.CLASS_NAME, "css-xrk2u6")
        save_button.click()
        wait_seconds(2)

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

                print(f"Updating product: {self.product_title}")
                print(f"For Author: {self.product_author}")

                self.init_driver()
                self.login_squarespace()
                self.load_product()
                self.add_additional_information()
                self.add_books_by_author()
                self.add_author_bio()
                self.add_sneak_peek_button()
                self.add_buy_amazon_button()
                self.add_buy_bella_button()
                self.add_paperbacks_text()
                self.add_books_by_author_text()
                self.add_spacers()
                self.save_work()

                print(f"Updated product: {self.product_title}")
                print(f"For Author: {self.product_author}")
                wait_seconds(5)


manager = SquarespaceManager()
# manager.init_driver()
# manager.login_squarespace()
# manager.load_product()
manager.update_products_from_csv()
# manager.update_custom_button()
# manager.add_additional_information()
# manager.add_books_by_author()
# manager.add_author_bio()
# manager.add_sneak_peek_button()
# manager.add_buy_amazon_button()
# manager.add_buy_bella_button()
# manager.add_paperbacks_text()
# manager.add_books_by_author_text()
# manager.add_spacers()
# manager.save_work()
