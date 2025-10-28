from selenium.webdriver.common.by import By 
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
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
    
    def click_copy_button(self):
        time.sleep(3)
        self.click_element(self.Locators.COPY_BTN)

    def get_email_address(self):
        return self._wait_for_visibility(self.Locators.EMAIL_FIELD).get_attribute("value")

