import pytest
from pages.home_page import Home
from pages.acount_page import Account

def test_login_via_password_succesfully(driver, load_data):
    home = Home(driver)

    home.go_to_account()
    assert home.is_on_account_screen(), "App should be on Account screen"

    account = Account(driver)
    account.click_login_with_email()
    assert account.click_login_via_password(), "Error to click in login with password button"

    assert load_data["login_credentials"]["correct_password"] != "", "Error: Enter the correct password in the JSON file"
    account.do_login_password_correctly(load_data)
    account.close_android_pop_up()
    assert home.is_on_account_screen(), "The site should be on Account Screen after login"

    assert account.click_edit_profile_info(), "Error to see account information"
    assert account.get_logged_email() == load_data["login_credentials"]["email"], f"Logged email should be {load_data['login_credentials']['email']}, but it is {account.get_logged_email()}"

