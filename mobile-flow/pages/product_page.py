from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class Product(BasePage):
    class Locators:
        SEARCH_BAR_FIELD = (AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.ImageView")
        FIRST_PRODUCT_RECOMEDATION = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'R$')][1]")
    
    def __init__(self,driver):
        super().__init__(driver)

    def is_product_name_correct(self, name):
        locator = (AppiumBy.ACCESSIBILITY_ID, name)
        return self.find_element(*locator)
    
    def is_product_price_correct(self, price):
        locator = (AppiumBy.XPATH,f"//*[@content-desc and contains(@content-desc, '{price}')]")
        return self.find_element(*locator)