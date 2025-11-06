from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class CartPopup(BasePage):
    class Locators:
        CARD_PRODUCT = (AppiumBy.XPATH, "//*[@resource-id='Card Produto']")
        QNTT_PRODUCT = (AppiumBy.XPATH, "//android.widget.EditText")
        PLUS_BTN= (AppiumBy.XPATH, "//android.widget.ImageView[@resource-id='Aumentar quantidade em 1']")
        MINUS_BTN= (AppiumBy.XPATH, "//android.widget.ImageView[@resource-id='Reduzir quantidade em 1']")
        ADD_TO_CART = (AppiumBy.XPATH, "//android.widget.Button[@content-desc='adicionar e continuar comprando']")

    def __init__(self,driver):
        super().__init__(driver)

    def is_product_name_correct(self, name):
        full_text = self.get_content_desc(*self.Locators.CARD_PRODUCT)
        if name in full_text:
            return True
        else:
            return False 

    def is_product_price_correct(self, price):
        full_text = self.get_content_desc(*self.Locators.CARD_PRODUCT)
        if price in full_text:
            return True
        else:
            return False 

    def get_product_quantity(self):
        return int(self.get_element_text(*self.Locators.QNTT_PRODUCT))
    
    def increase_qunatity(self):
        return self.click_element(*self.Locators.PLUS_BTN)

    def decrease_qunatity(self):
        return self.click_element(*self.Locators.MINUS_BTN)

    def decrease_quantity_untill_X(self, x):
        while self.get_product_quantity() > x:
            self.decrease_qunatity()
        
    def increase_quantity_untill_X(self, x):
        while self.get_product_quantity() < x:
            self.increase_qunatity()

    def add_to_cart(self):
        return self.click_element(*self.Locators.ADD_TO_CART)

