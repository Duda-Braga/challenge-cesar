import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage

@pytest.mark.web_test
def test_login_via_password_succesfully(driver, load_data):

    home = HomePage(driver)
    home.navigate()
    home.close_promotion_banner()
    home.go_to_login()
        
    login = LoginPage(driver)
    assert login.is_on_login_page(), "The site is not on the login screen"
    assert login.clcik_on_login_via_password(), "Error to clicl in login with password button"

    assert load_data["login_credentials"]["correct_password"] != "", "Error: Enter the correct password in the JSON file"
    
    login.do_login_password_correctly(load_data)
    assert home.is_on_home_page(), "The site should be on home page after login"
    home.close_promotion_banner()

    assert home.get_logged_email() == load_data["login_credentials"]["email"], f"Logged email should be {load_data['login_credentials']['email']}, but it is {home.get_logged_email()}"


