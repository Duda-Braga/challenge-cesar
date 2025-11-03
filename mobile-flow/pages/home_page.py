from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class Home(BasePage):
    class Locators:
        SEARCH_BAR = (AppiumBy.ACCESSIBILITY_ID, "busque aqui seu produto")
        HOME_ICON = (AppiumBy.ACCESSIBILITY_ID, "Home\nTab 1 of 5")
        ACCOUNT_ICON = (AppiumBy.ID,"Conta\nTab 5 of 5")
        #promation banner
        # BANNER_CONTAINER = (AppiumBy.CLASS_NAME, "android.app.Dialog")
        # CLOSE_BANNER = (AppiumBy.CLASS_NAME, "android.widget.Button")
        # CLOSE_BUTTON_TEXT = "Close"

    def __init__(self,driver):
        super().__init__(driver)
    
    def is_on_home_screen(self):
        return self.is_element_selected(*self.Locators.HOME_ICON)
    
    def go_to_home(self):
        self.click_element(*self.Locators.HOME_ICON)

    def go_to_serach_page(self):
        self.click_element(*self.Locators.SEARCH_BAR)

