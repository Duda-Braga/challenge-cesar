import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage

def test_login_with_wrong_password(driver, load_data):

    home = HomePage(driver)
    home.navigate()
    home.close_promotion_banner()
    home.go_to_login()
        
    login = LoginPage(driver)
    assert login.is_on_login_page(), "The site is not on the login screen"
    assert login.clcik_on_login_via_password(), "Error to clicl in login with password button"

    login.do_login_password_incorrectly(load_data)
    assert login.is_login_error_message_on_screen(), "Message error should be displayed if the login is not successful"
