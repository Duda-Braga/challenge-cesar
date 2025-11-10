import pytest
from pages.home_page import Home
from pages.acount_page import Account


@pytest.mark.mobile_test
def test_login_with_wrong_password(driver, load_data):
    home = Home(driver)

    home.go_to_account()
    assert home.is_on_account_screen(), "App should be on Account screen"

    account = Account(driver)
    account.click_login_with_email()
    assert account.click_login_via_password(), "Error to click in login with password button"

    assert account.do_login_password_incorrectly(load_data), "Error to do wrong login"
    assert account.is_login_error_message_on_screen(), "Message error should be displayed when the login is not successful"