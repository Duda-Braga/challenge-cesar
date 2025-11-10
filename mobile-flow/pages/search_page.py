from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import time

class Search(BasePage):
    class Locators:
        SEARCH_BAR_FIELD = (AppiumBy.XPATH, "(//android.view.View[1]/android.widget.ImageView)[1]")
        FIRST_PRODUCT_RECOMEDATION = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'R$')][1]")

    def __init__(self,driver):
        super().__init__(driver)

    def click_search_field(self):
        self.click_element(*self.Locators.SEARCH_BAR_FIELD)
        
    def search_element(self, text): 
        self.click_search_field()
        self.send_keys_to_element(*self.Locators.SEARCH_BAR_FIELD, text)


    def click_on_first_product(self):
        time.sleep(2)
        return self.click_element(*self.Locators.FIRST_PRODUCT_RECOMEDATION)
    
    def search_element_enter(self, text): 
        self.click_search_field()
        self.send_keys_to_element(*self.Locators.SEARCH_BAR_FIELD, text)
        self.driver.press_keycode(66)
        