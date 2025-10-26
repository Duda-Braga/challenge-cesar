from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage


class Login(BasePage):
    class Locators:
        LOGIN_TITLE = (By.XPATH, "//h2[text()='login do cliente']")
        LOGIN_FIELD = (By.CSS_SELECTOR, "input[name='email']")
        SEND_BTN = (By.CSS_SELECTOR, "button[type='submit']")
        
    def __init__(self, driver):
        super().__init__(driver)

    def is_on_login_page(self):
        return self.is_element_displayed(self.Locators.LOGIN_TITLE)
    
    def fill_email_field(self):
        email = "aa@gmail.com"
        self.send_keys_to_element(self.Locators.LOGIN_FIELD, email)
    
    def send_email(self):
        self.click_element(self.Locators.SEND_BTN)