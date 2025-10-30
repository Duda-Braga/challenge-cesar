from selenium.webdriver.common.by import By 
from .base_page import BasePage 

from config import TEMP_EMAIL_URL 
import time
class TempMailPage(BasePage):
    """
    temporary email site
    """
    class Locators:
        EMAIL_FIELD = (By.CSS_SELECTOR, 'input[data-qa="current-email"]')
        COPY_BTN = (By.CSS_SELECTOR, "button[data-qa='copy-button']")
        REFRESH_BTN = (By.CSS_SELECTOR, "button[data-qa='refresh-button']")
        EMAIL_SUBJECT_TXT = (By.CSS_SELECTOR, "span[data-qa='message-subject']")
    
    def navigate(self):
        self.driver.execute_script(f"window.open('{TEMP_EMAIL_URL}');")

    def click_copy_button(self):
        time.sleep(3)
        return self.click_element(self.Locators.COPY_BTN)

    def get_email_address(self):
        return self._wait_for_visibility(self.Locators.EMAIL_FIELD).get_attribute("value")

    def click_refresh_button(self):
        return self.click_element(self.Locators.REFRESH_BTN)
    
    def get_email_code(self):
        complete_text = self.get_element_text(self.Locators.EMAIL_SUBJECT_TXT)
        if complete_text != "":
            return complete_text[-6:]
        else: return ""