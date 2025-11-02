from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage

import time
class MyAccount(BasePage):
    class Locators:
        PROFILE_EMAIL = ((By.XPATH, "//label[text()='Email']/ancestor::div[1]/div[contains(@class, 'dataEntryChildren')]"))
        
        AUTHENTICATION_BTN = (By.CSS_SELECTOR, "a[href='#/authentication']")
        SET_PASSWORD_BTN = (By.XPATH, "//button[contains(., 'Definir senha')]")
        SET_PASSWORD_CODE_FIELD = (By.XPATH, "//span[text()='Código']/ancestor::label[1]//input")
        PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")
        SAVE_PASSWORD_BTN = (By.XPATH, "//button[contains(., 'Salvar senha')]")
        SAVED_PASSWORD_HIDDEN = (By.CSS_SELECTOR, "div.vtex-my-authentication-1-x-maskedPassword_content")

    def get_profile_email(self):
        return self.get_element_text(self.Locators.PROFILE_EMAIL)
    
    def click_on_authentication(self):
        return self.click_element(self.Locators.AUTHENTICATION_BTN)
    
    def click_set_password(self):
        return self.click_element(self.Locators.SET_PASSWORD_BTN)
    
    def fill_set_password_code(self, code):
        return self.send_keys_to_element(self.Locators.SET_PASSWORD_CODE_FIELD, code)
    
    def fill_password_field_less_8_char(self, load_data):
        self.clear_field_element(self.Locators.PASSWORD_FIELD)
        return self.send_keys_to_element(self.Locators.PASSWORD_FIELD, load_data["password_scenarios"]["less_8_char"])
    
    def fill_password_field_no_number(self, load_data):
        self.clear_field_element(self.Locators.PASSWORD_FIELD)
        return self.send_keys_to_element(self.Locators.PASSWORD_FIELD, load_data["password_scenarios"]["no_numbers"])
    
    def fill_password_field_no_lowerchar(self, load_data):
        self.clear_field_element(self.Locators.PASSWORD_FIELD)
        return self.send_keys_to_element(self.Locators.PASSWORD_FIELD, load_data["password_scenarios"]["no_lowercase"])
    
    def fill_password_field_no_upperchar(self, load_data):
        self.clear_field_element(self.Locators.PASSWORD_FIELD)
        return self.send_keys_to_element(self.Locators.PASSWORD_FIELD, load_data["password_scenarios"]["no_uppercase"])
    
    def fill_password_field_correctly(self, load_data):
        self.clear_field_element(self.Locators.PASSWORD_FIELD)
        return self.send_keys_to_element(self.Locators.PASSWORD_FIELD, load_data["password_scenarios"]["strong_pass"])
    
    def is_save_password_btn_inactive(self):
        return not self.is_element_enabled(self.Locators.SAVE_PASSWORD_BTN)
    
    def is_save_password_btn_activate(self):
        return self.is_element_enabled(self.Locators.SAVE_PASSWORD_BTN)
    
    def click_save_password_button(self):
        return self.click_element(self.Locators.SAVE_PASSWORD_BTN)

    def is_new_password_saved(self):
        return self._find_element(self.Locators.SAVED_PASSWORD_HIDDEN)
    
    