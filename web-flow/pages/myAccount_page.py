from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage

class MyAccount(BasePage):
    class Locators:
        MY_ACCOUNT_TITLE = (By.CSS_SELECTOR, "div.vtex-my-account-1-x-userGreeting")
        REGISTER_SIDE_BAR = (By.XPATH, "//a[text()='Dados pessoais']")

    def is_on_my_account_page(self):
        #error
        return self.is_element_displayed(self.Locators.MY_ACCOUNT_TITLE)
    
    def click_on_register(self):
        return self.click_element(self.Locators.REGISTER_SIDE_BAR)