from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class Home(BasePage):
    class Locators:
        SEARCH_BAR = (AppiumBy.ID," ")
        HOME_ICON = (AppiumBy.ID," ")
        ACCOUNT_ICON = (AppiumBy.ID," ")
        #promation banner
        CLOSE_BANNER = (AppiumBy.CLASS_NAME, "android.widget.Button")
        BANNER = (AppiumBy.CLASS_NAME, "android.widget.Button")
        
    def __init__(self,driver):
        super().__init__(driver)
    
    def is_on_home_page(self):
        return self.is_element_selected(*self.Locators.HOME_ICON)

    def close_banner(self):
        if self.is_element_displayed(*self.Locators.BANNER):
            self.click_element(*self.Locators.CLOSE_BANNER)

    def search_product(self, load_data): #create load data function with api info
        #see if it changes if you click before
        #self.click_element(AppiumBy.ID, *self.Locators.SEARCH_BAR)
        self.send_keys_to_element(AppiumBy.ID, *self.Locators.SEARCH_BAR, load_data[""])
    