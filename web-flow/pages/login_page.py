from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException#
from .base_page import BasePage

class LoginPage(BasePage):
    class Locators:
        LOGIN_TITLE = (By.XPATH, "//h2[text()='login do cliente']")
        LOGIN_FIELD = (By.CSS_SELECTOR, "input[name='email']")
        SEND_BTN = (By.CSS_SELECTOR, "button[type='submit']")
        CODE_FIELD = (By.CSS_SELECTOR, "input[name='token']")
        CONFIRM_CODE_BTN = (By.CSS_SELECTOR, "button[type='submit']")

        LOGIN_VIA_PASSWORDL_BTN =(By.XPATH, "//button[contains(., 'Entrar com email e senha')]")
        #(By.CSS_SELECTOR, "button[type='button']")
        EMAIL_FIELD = (By.CSS_SELECTOR, "input[placeholder*='exemplo@mail.com']")
        PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")
        ENTER_BTN = (By.XPATH, "//button[contains(., 'Entrar')]")
        ERROR_LOGIN_PASSWORD = (By.XPATH,"//div[@role='alert' and text()='Usuário e/ou senha incorretos']")
        
    def __init__(self, driver):
        super().__init__(driver)

    def is_on_login_page(self):
        return self.is_element_displayed(self.Locators.LOGIN_TITLE)
    
    def fill_email_field(self, text):
        return self.send_keys_to_element(self.Locators.LOGIN_FIELD, text)
        
    def paste_on_email_filed(self):
        paste = (Keys.CONTROL, "v")
        return self.send_keys_to_element(self.Locators.LOGIN_FIELD, paste)
    
    def enter_email(self):
        return self.send_keys_to_element(self.Locators.LOGIN_FIELD, (Keys.ENTER))

    def send_email(self):
        return self.click_element(self.Locators.SEND_BTN)
    
    def fill_code_field(self, text):
        return self.send_keys_to_element(self.Locators.CODE_FIELD, text)
    
    def enter_code(self):
        return self.send_keys_to_element(self.Locators.CODE_FIELD, (Keys.ENTER))
    
    def send_code(self):
        return self.click_element(self.Locators.CONFIRM_CODE_BTN)

    # def clcik_on_login_via_password(self):
    #     return self.click_element(self.Locators.LOGIN_VIA_PASSWORDL_BTN)

    def clcik_on_login_via_password(self) -> bool:
        """
        intercepeted click fix
        """
        locator = self.Locators.LOGIN_VIA_PASSWORDL_BTN
        
        try:
            if self.click_element(locator):
                return True
            
            return False

        except ElementClickInterceptedException:
            # FALLBACK JS 
            print(f"Warning: Click intercepted on {locator}")
            
            element = self._wait_for_clickable(locator)
            
            if element:
                try:
                    self.driver.execute_script("arguments[0].click();", element)
                    return True
                except Exception as e:
                    # failed with JS
                    print(f"JavaScript error when clicking: {e}")
                    return False
            
            return False
            
        except Exception as e:
            return False
    
    def fill_password_field(self, text):
        return self.send_keys_to_element(self.Locators.PASSWORD_FIELD, text)
    
    def fill_email_with_pass_field(self, text):
        return self.send_keys_to_element(self.Locators.EMAIL_FIELD, text)
    
    def do_login_password_correctly(self, load_data):
        self.fill_email_with_pass_field(load_data["login_credentials"]["email"])
        self.fill_password_field(load_data["login_credentials"]["correct_password"])
        self.click_element(self.Locators.ENTER_BTN)

    def do_login_password_incorrectly(self, load_data):
        self.fill_email_with_pass_field(load_data["login_credentials"]["email"])
        self.fill_password_field(load_data["login_credentials"]["wrong_password"])
        self.click_element(self.Locators.ENTER_BTN)
    
    def is_login_error_message_on_screen(self):
        return self.is_element_displayed(self.Locators.ERROR_LOGIN_PASSWORD)