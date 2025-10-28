from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from .base_page import BasePage


class LoginPage(BasePage):
    class Locators:
        LOGIN_TITLE = (By.XPATH, "//h2[text()='login do cliente']")
        LOGIN_FIELD = (By.CSS_SELECTOR, "input[name='email']")
        # SEND_BTN = (By.CSS_SELECTOR, "button[type='submit']")
        SEND_BTN = (By.XPATH, "//button[.//span[text()='Enviar']]")
        
    def __init__(self, driver):
        super().__init__(driver)

    def is_on_login_page(self):
        return self.is_element_displayed(self.Locators.LOGIN_TITLE)
    
    def fill_email_field(self, text):
        return self.send_keys_to_element(self.Locators.LOGIN_FIELD, text)
        
    def paste_on_email_filed(self):
        paste = (Keys.CONTROL, "v")
        return self.send_keys_to_element(self.Locators.LOGIN_FIELD, paste)
    
    def enter_email(self):
        return self.send_keys_to_element(self.Locators.LOGIN_FIELD, (Keys.ENTER))

    def send_email(self):
        return self.click_element(self.Locators.SEND_BTN)