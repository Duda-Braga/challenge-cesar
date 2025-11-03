from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.mobile_gestures import MobileGestures 
from selenium.common.exceptions import TimeoutException


class BasePage:
    '''
    Common methods for all pages
    '''
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.gestures = MobileGestures(driver) 

    def find_element(self, by, locator):
        try:
            return self.wait.until(EC.presence_of_element_located((by, locator)))
        except TimeoutException:
            # did not found element
            return False
    
    def wait_for_visibility_of_element(self, by, locator): 
        try: 
            return self.wait.until(EC.visibility_of_element_located((by, locator)))
        except TimeoutException: 
            return False 
    
    def wait_for_element_to_be_clickable(self, by, locator): 
        try:
            return self.wait.until(EC.element_to_be_clickable((by, locator)))
        except TimeoutException: 
            return False 
    
    def click_element(self, by, locator):
        element = self.wait_for_element_to_be_clickable(by, locator)
        if element is not False: 
            try: 
                element.click()
                return True 
            except Exception: 
                return False 
        return False 
    
    def send_keys_to_element(self, by, locator, text):
        element = self.wait_for_visibility_of_element(by, locator)
        if element is not False: 
            try: 
                element.clear() 
                element.send_keys(text)
                return True 
            except Exception:
                return False 
        return False
        
    def get_element_text(self, by, locator):
        element = self.wait_for_visibility_of_element(by, locator)
        if element is not False: 
            try: 
                return element.text
            except Exception:
                return "" 
        return "" 

    def is_element_displayed(self, by, locator):
        element = self.find_element(by, locator) 
        if element is not False: 
            try:
                return element.is_displayed()
            except Exception:
                return False 
        return False
    
    def is_element_enabled(self, by, locator):
        element = self.find_element(by, locator) 
        if element is not False: 
            try:
                return element.is_enabled()
            except Exception:
                return False
        return False 

    def is_element_checked(self, by, locator):
        element = self.find_element(by, locator) 
        if element is not False: 
            try:
                return element.get_attribute("checked") is not None 
            except Exception:
                return False
        return False 
    
    def is_element_selected(self, by, locator):
        element = self.find_element(by, locator)
        if element is not False: 
            try:
                return element.is_selected() 
            except Exception:
                return False
        return False
    
    def scroll_untill_is_visible(self, by, locator, way, max_scroll):
        for i in range(max_scroll):
            try:
                element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((by, locator)))
                if element.is_displayed():
                    return True
                
            except :
                pass  
            
            self.gestures.scroll_screen(direction=way)
        return False
    

