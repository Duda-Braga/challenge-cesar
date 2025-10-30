import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver 
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config import DEFAULT_TIMEOUT

class BasePage:
    """
    common methods to all page objects
    """
    
    def __init__(self, driver):
        """
        Initializes the WebDriver instance and the explicit wait object (WebDriverWait)
        The driver is assumed to be an initialized Selenium WebDriver instance
        """
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(self.driver, DEFAULT_TIMEOUT)


    def _find_element(self, by_locator):
        try:
            return self.wait.until(EC.presence_of_element_located(by_locator))
        except (TimeoutException, NoSuchElementException):
            return None

    def _wait_for_visibility(self, by_locator): 
        try: 
            return self.wait.until(EC.visibility_of_element_located(by_locator))
        except (TimeoutException, NoSuchElementException): 
            return None
        
    def _wait_for_clickable(self, by_locator):
        try:
            return self.wait.until(EC.element_to_be_clickable(by_locator))
        except (TimeoutException, NoSuchElementException): 
            return None

        

    def click_element(self, by_locator):
        element = self._wait_for_clickable(by_locator)
        if element: 
            element.click()
            return True 
        return False
    
    def send_keys_to_element(self, by_locator, text):
        element = self._wait_for_visibility(by_locator)
        if element: 
            element.send_keys(text)
            return True 
        return False


    def is_element_displayed(self, by_locator):
        element = self._wait_for_visibility(by_locator) 
        if element: 
            return True 
        return False

    def get_element_text(self, by_locator):
        element = self._wait_for_visibility(by_locator)
        if element: 
            return element.text
        return ""


    def go_to_last_tab(self):
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        time.sleep(2)

    def go_to_first_tab(self):
        main_window_handle = self.driver.window_handles[0]
        self.driver.switch_to.window(main_window_handle)
        time.sleep(2)
