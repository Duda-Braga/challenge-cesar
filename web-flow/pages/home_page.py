from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from .base_page import BasePage
from config import BASE_URL 
import time

class HomePage(BasePage):
    """
    Inicial Americans Pages
    """
    class Locators:
        LOGIN_BTN = (By.CSS_SELECTOR, "a[aria-label='link para a página de login']")
        LOGIN_NAME = (By.XPATH, "//span[contains(text(),'olá,')]")

        # promotion Locators
        PROMOTION_BANNER = (By.CLASS_NAME, "show-element")
        CLOSE_BANNER_BTN = (By.CSS_SELECTOR, ".show-element [aria-label='Fechar']")

    def __init__(self, driver):
        super().__init__(driver)

    def navigate(self):
        self.driver.get(BASE_URL)

    def is_on_home_page(self):
        time.sleep(2)
        actual_url = self.driver.current_url
        if actual_url == BASE_URL: return True
        else: return False 
    
    def close_promotion_banner(self):
        """
        close the banner, if the banner does not appear, continue the code without error
        """
        temp_wait = WebDriverWait(self.driver, 5) 

        try:
            temp_wait.until(EC.element_to_be_clickable(self.Locators.PROMOTION_BANNER)).click()
            
        except TimeoutException:
            #test continues
            print("banner not found")
        
    def go_to_login(self):
        self.click_element(self.Locators.LOGIN_BTN)
        time.sleep(2)

    def get_logged_email(self):
        time.sleep(2)
        complete_text =  self.get_element_text(self.Locators.LOGIN_NAME)
        if complete_text == "": return ""
        else:
            return complete_text[5:] #remove 'ola, ' part
        
    def go_to_my_account(self):
        return self.click_element(self.Locators.LOGIN_NAME)