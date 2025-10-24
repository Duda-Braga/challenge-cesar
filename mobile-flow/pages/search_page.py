from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
from selenium.webdriver.common.keys import Keys
class Search(BasePage):
    class Locators:
        SEARCH_BAR_FIELD = (AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.ImageView")

    def __init__(self,driver):
        super().__init__(driver)

    def click_search_field(self):
        self.click_element(*self.Locators.SEARCH_BAR_FIELD)
        
    def search_element(self, load_data, cont=0): #cont temporary
        self.click_search_field()
        self.send_keys_to_element(*self.Locators.SEARCH_BAR_FIELD, load_data["products"][cont]["Product"])
        #self.find_element(*self.Locators.SEARCH_BAR_FIELD).submit() TODO
        #self.send_enter_to_element(*self.Locators.SEARCH_BAR_FIELD)