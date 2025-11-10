from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class Cart(BasePage):
    class Locators:
        TOTAL_NAME_PRICE = (AppiumBy.XPATH, "//android.view.View[@content-desc='Total']")
        TOTAL_PRICE = (AppiumBy.XPATH, "//android.view.View[@content-desc='Total']/following-sibling::android.view.View[contains(@content-desc, 'R$')][1]")
        SUBTOTAL_PRICE = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Subtotal')]/following-sibling::android.view.View[contains(@content-desc, 'R$')][1]")
        CHECKOUT_AREA = (AppiumBy.XPATH, "//android.view.View[starts-with(@content-desc, 'fechar pedido')]")
        TYPE_CEP_FIELD = (AppiumBy.XPATH, '//android.widget.EditText[@resource-id="Digite o CEP"]')
        ERROR_MSG = (AppiumBy.XPATH, "//android.view.View[@content-desc='Campo obrigatório']")
        CALCULATE_FRETE_BTN = (AppiumBy.XPATH, "//android.widget.Button[@content-desc='Calcular']")
        CLEAR_FRETE_BTN = (AppiumBy.XPATH, "//android.widget.Button[@content-desc='Apagar cep pesquisado']")
        FRETE_PRICE_MSG = (AppiumBy.XPATH, "//android.view.View[contains(@content-desc, 'Receba em até ')]")
        REDIRECTED_MESSAGE = (AppiumBy.XPATH, "//android.view.View[@content-desc='Informe seu e-mail para continuar']")


    def __init__(self,driver):
        super().__init__(driver)

    def is_product_name_correct(self, name):
        locator = (AppiumBy.ACCESSIBILITY_ID, name)
        return self.find_element(*locator)
    
    def is_product_quantity_correct(self, qtt):
        locator = (AppiumBy.XPATH, f"//android.widget.EditText[@text='{qtt}']")
        return self.find_element(*locator)

    def find_total_price(self):
        self.scroll_untill_is_visible(*self.Locators.TOTAL_NAME_PRICE, "down", 5)

    def get_subtotal_price(self):
        value = self.get_content_desc(*self.Locators.SUBTOTAL_PRICE)
        if value == "":
            return ""
        value = value.replace("R$", "").replace("\xa0", "").strip()
        value = value.replace(".", "")
        value = value.replace(",", ".")
        return float(value)

    def get_total_price(self):
        value = self.get_content_desc(*self.Locators.TOTAL_PRICE)
        if value == "":
            return ""
        value = value.replace("R$", "").replace("\xa0", "").strip()
        value = value.replace(".", "")
        value = value.replace(",", ".")
        return float(value)
    
    def get_ckecout_price(self):
        full_text = self.get_content_desc(*self.Locators.CHECKOUT_AREA)
        if full_text == "":
            return ""
        value = full_text.split('R$')[-1]
        value = value.replace('.', '').strip()
        value = value.replace(',', '.')
        return float(value)
    
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
    

    def proceed_to_checkout(self):
        self.click_element(*self.Locators.CHECKOUT_AREA)

    def check_redirection(self):
        return self.find_element(*self.Locators.REDIRECTED_MESSAGE)
    