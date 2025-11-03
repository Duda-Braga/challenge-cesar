import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.tempEmail_page import TempMailPage
from pages.myAccount_page import MyAccount

def test_new_user_registration_and_password_setup(driver, load_data):

    home = HomePage(driver)
    home.navigate()
    home.close_promotion_banner()
    home.go_to_login()
    
    login = LoginPage(driver)
    assert login.is_on_login_page(), "The site is not on the login screen"

    tempEmail = TempMailPage(driver)
    tempEmail.navigate()
    tempEmail.go_to_last_tab()
    tempEmail.click_copy_button()
    temporary_email = tempEmail.get_email_address()
    assert temporary_email != "", "Failed to retrieve temporary email"

    tempEmail.go_to_first_tab()
    login.fill_email_field(temporary_email)
    assert login.enter_email(), "Error to send email"


    tempEmail.go_to_last_tab()
    tempEmail.click_refresh_button()
    access_code = tempEmail.get_email_code()
    assert access_code != "", "Error to get access code"
    
    tempEmail.go_to_first_tab()
    login.fill_code_field(access_code)
    assert login.enter_code(), "Error to send access code"
    
    assert home.is_on_home_page(), "The site should be on home page after login"
    home.close_promotion_banner()

    assert home.get_logged_email() == temporary_email, f"Logged email should be {temporary_email}, but it is {home.get_logged_email()}"
    assert home.go_to_my_account(), "Error to go to My Account page"

    myAccount = MyAccount(driver)
    assert myAccount.get_profile_email() == temporary_email, f"Wrong email in the registration tab. It should be {temporary_email} but it is {myAccount.get_profile_email()}"
    assert myAccount.click_on_authentication(), "Error to go to authentication area on My Account page"
    myAccount.click_set_password(), "Error to click set password"

    tempEmail.go_to_last_tab()
    tempEmail.click_refresh_button()
    set_password_code = tempEmail.get_email_code()
    assert set_password_code != "", "Error to get password definition code"
    while(set_password_code == access_code): #same email
        set_password_code = tempEmail.get_email_code()
        tempEmail.click_refresh_button()
    tempEmail.go_to_first_tab()

    assert myAccount.fill_set_password_code(set_password_code), "Error to type set password code on authentication My Account page"
    
    myAccount.fill_password_field_less_8_char(load_data)
    assert myAccount.is_save_password_btn_inactive(), "The 'Save' button should be inactivate because the password is less than 8 characters"

    myAccount.fill_password_field_no_number(load_data)
    assert myAccount.is_save_password_btn_inactive(), "The 'Save' button should be inactivate because the password is missing numbers"
    
    myAccount.fill_password_field_no_lowerchar(load_data)
    assert myAccount.is_save_password_btn_inactive(), "The 'Save' button should be inactivate because the password is missings lowercase letters"

    myAccount.fill_password_field_no_upperchar(load_data)
    assert myAccount.is_save_password_btn_inactive(), "The 'Save' button should be inactivate because the password is missing uppercase letters"

    myAccount.fill_password_field_correctly(load_data)
    assert myAccount.is_save_password_btn_activate(), "The 'Save' button should be activate for a valid password"
    myAccount.click_save_password_button()

    assert myAccount.is_new_password_saved(), "The password was not saved successfully"