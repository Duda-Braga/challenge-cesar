from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage
import time
class Account(BasePage):
    class Locators:
        ENTER_EMAIL_BTN = (AppiumBy.XPATH, "//android.view.View[@resource-id='Entrar com e-mail']")
        ENTER_PASSWORD_BTN = (AppiumBy.XPATH, "//android.widget.Button[@content-desc='Entrar com e-mail e senha']")
        EMAIL_FIELD = (AppiumBy.XPATH, "//android.widget.EditText[@resource-id='E-mail']")
        PASSWORD_FIELD = (AppiumBy.XPATH, "//android.widget.EditText[@resource-id='Senha']")
        ENTER_BTN = (AppiumBy.XPATH, "//android.view.View[@resource-id='Entrar']")
        ERROR_LOGIN_PASSWORD = (AppiumBy.XPATH, "(//android.view.View[@content-desc='Usuário ou senha inválidos.'])")

        EDIT_PROFILE_BTN = (AppiumBy.XPATH, "//android.view.View[@content-desc='Editar dados pessoais']")
        REGISTRED_EMAIL = (AppiumBy.XPATH, "//android.view.View[@resource-id='E-mail']")

        SAVE_PASSWORD_POPUP = (AppiumBy.XPATH, "//android.widget.Button[@resource-id='android:id/autofill_save_no']")

    def __init__(self,driver):
        super().__init__(driver)
    
    def click_login_with_email(self):
        self.click_element(*self.Locators.ENTER_EMAIL_BTN)

    def click_login_via_password(self):
        return self.click_element(*self.Locators.ENTER_PASSWORD_BTN)

    def fill_password_field(self, text):
        self.click_element(*self.Locators.PASSWORD_FIELD)
        return self.send_keys_to_element(*self.Locators.PASSWORD_FIELD, text)
    
    def fill_email_with_pass_field(self, text):
        self.click_element(*self.Locators.EMAIL_FIELD)
        return self.send_keys_to_element(*self.Locators.EMAIL_FIELD, text)
    
    def do_login_password_correctly(self, load_data):
        self.fill_email_with_pass_field(load_data["login_credentials"]["email"])
        self.fill_password_field(load_data["login_credentials"]["correct_password"])
        self.click_element(*self.Locators.ENTER_BTN)

    def do_login_password_incorrectly(self, load_data):
        self.fill_email_with_pass_field(load_data["login_credentials"]["email"])
        self.fill_password_field(load_data["login_credentials"]["wrong_password"])
        return self.click_element(*self.Locators.ENTER_BTN)
    
    def is_login_error_message_on_screen(self):
        return self.is_element_displayed(*self.Locators.ERROR_LOGIN_PASSWORD)

    def click_edit_profile_info(self):
        return self.click_element(*self.Locators.EDIT_PROFILE_BTN)
    
    def get_logged_email(self):
        return self.get_element_text(*self.Locators.REGISTRED_EMAIL)
    
    def close_android_pop_up(self):
        self.click_element(*self.Locators.SAVE_PASSWORD_POPUP)