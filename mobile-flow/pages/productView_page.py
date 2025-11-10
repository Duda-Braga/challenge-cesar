from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import time

class ProductView(BasePage):
    class Locators:
        TYPE_OF_VISUALIZATION_BTN = (AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.ImageView[2]")

    def __init__(self,driver):
        super().__init__(driver)
    
    def change_type_of_visualization(self):
        return self.click_element(*self.Locators.TYPE_OF_VISUALIZATION_BTN)

    def is_product_name_correct(self, product_name):
        locator = (AppiumBy.XPATH, f"//android.view.View[contains(@content-desc, '{product_name}')]")
        return self.find_element(*locator)
        
    def is_product_price_correct(self, name, price):
        locator = (AppiumBy.XPATH, f"//android.view.View[contains(@content-desc, '{name}')]")
        full_text = self.get_content_desc(*locator)

        parts = full_text.split("R$")
        last_part = parts[-1]
        final_price = last_part.split('\n')[0]
        actual_price = final_price.strip()

        if actual_price == price:
            return True
        else:
            return False  
        
    
    def click_product(self, product_name):
        locator = (AppiumBy.XPATH, f"//android.view.View[contains(@content-desc, '{product_name}')]")
        self.click_element(*locator)
