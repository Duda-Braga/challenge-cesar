from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.mobile_gestures import MobileGestures 

class BasePage:
    '''
    Common methods for all pages
    '''
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.gestures = MobileGestures(driver) 

    def find_element(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))
    
    def wait_for_visibility_of_element(self, by, locator):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))
    
    def wait_for_element_to_be_clickable(self, by, locator):
        return self.wait.until(EC.element_to_be_clickable((by, locator)))
    
    def click_element(self, by, locator):
        self.wait_for_element_to_be_clickable(by, locator).click()

    def send_keys_to_element(self, by, locator, text):
        self.wait_for_visibility_of_element(by, locator).send_keys(text)

    def get_element_text(self, by, locator):
        return self.wait_for_visibility_of_element(by, locator).text

    def is_element_displayed(self, by, locator):
        try:
            return self.find_element(by, locator).is_displayed()
        except:
            return False
    
    def is_element_enabled(self, by, locator):
        return self.find_element(by, locator).is_enabled()

    def is_element_checked(self, by, locator):
        return self.find_element(by, locator).get_attribute("checked")
    
    def is_element_selected(self, by, locator):
        return self.find_element(by, locator).get_attribute("selected")
    
    def scroll_untill_is_visible(self, by, locator, way, max_scroll):
        for i in range(max_scroll):
            try:
                element = WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((by, locator)))
                if element.is_displayed():
                    return True
                
            except :
                pass  
            
            self.gestures.scroll_screen(direction=way)