from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class Product(BasePage):
    class Locators:
        SEARCH_BAR_FIELD = (AppiumBy.XPATH, "//android.widget.FrameLayout[@resource-id='android:id/content']/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.widget.ImageView")
        FIRST_PRODUCT_RECOMEDATION = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'R$')][1]")
        TYPE_CEP_FIELD = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="Digite o CEP"]')
        ERROR_MSG = (AppiumBy.XPATH, "//android.view.View[@content-desc='Campo obrigatório']")
        CALCULATE_FRETE_BTN = (AppiumBy.XPATH, "//android.widget.Button[@content-desc='Calcular']")
        CLEAR_FRETE_BTN = (AppiumBy.XPATH, "//android.widget.Button[@content-desc='Apagar cep pesquisado']")
        FRETE_PRICE_MSG = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Receba em até ')]")
        BUY_BTN = (AppiumBy.XPATH, "//android.view.View[@content-desc='comprar']")


    def __init__(self,driver):
        super().__init__(driver)

    def is_product_name_correct(self, name):
        locator = (AppiumBy.ACCESSIBILITY_ID, name)
        return self.find_element(*locator)
    
    def is_product_price_correct(self, price):
        locator = (AppiumBy.XPATH,f"//*[@content-desc and contains(@content-desc, '{price}')]")
        return self.find_element(*locator)
    
    def find_zip_field(self):
        self.scroll_untill_is_visible(*self.Locators.TYPE_CEP_FIELD, "down", 2)

    def fill_invalid_zip_code(self):
        self.click_element(*self.Locators.TYPE_CEP_FIELD)
        self.send_keys_to_element(*self.Locators.TYPE_CEP_FIELD, "123456")
        self.click_element(*self.Locators.CALCULATE_FRETE_BTN)

    def fill_valid_zip_code(self, code):
        self.click_element(*self.Locators.TYPE_CEP_FIELD)
        self.send_keys_to_element(*self.Locators.TYPE_CEP_FIELD, code)
        self.click_element(*self.Locators.CALCULATE_FRETE_BTN)

    def clear_zip_code_field(self):
        return self.click_element(*self.Locators.CLEAR_FRETE_BTN)

    def is_error_message_on_screen(self):
        return self.find_element(*self.Locators.ERROR_MSG)
    
    def is_delivery_time_on_screen(self):
        return self.find_element(*self.Locators.FRETE_PRICE_MSG)
    
    def get_shipping_cost(self):
        full_text = self.get_content_desc(*self.Locators.FRETE_PRICE_MSG)
        if full_text == "":
            return ""
        parts = full_text.split(': ')
        
        if len(parts) > 1:
            price_part = parts[1].strip()
            if "R$" in price_part:
                price_parts = price_part.split("R$")
                return price_parts[-1].strip()
            else: # freee
                return price_part         
        return ""
            
    def get_delivery_time(self):
        full_text = self.get_content_desc(*self.Locators.FRETE_PRICE_MSG)
        if full_text == "":
            return ""
        parts = full_text.split(': ')
        
        if len(parts) > 1:
            time_part = parts[0].split("até ")
            if len(time_part) > 1:
                time = time_part[-1]
                return time   
        return ""
    
    def click_on_buy_product(self):
        self.click_element(*self.Locators.BUY_BTN)