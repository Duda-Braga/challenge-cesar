import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver 

from config import DEFAULT_TIMEOUT

class BasePage:
    """
    communn methods to all page objects
    """
    
    def __init__(self, driver):
        """
        Initializes the WebDriver instance and the explicit wait object (WebDriverWait)
        The driver is assumed to be an initialized Selenium WebDriver instance
        """
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)



    def _find_element(self, by_locator):
        return self.wait.until(EC.visibility_of_element_located(by_locator))

    def _find_clickable_element(self, by_locator: tuple):
        return self.wait.until(EC.element_to_be_clickable(by_locator))
    
    def click_element(self, by_locator):
        self._find_clickable_element(by_locator).click()


