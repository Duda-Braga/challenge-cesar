import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.tempEmail_page import TempMailPage
from pages.myAccount_page import MyAccount
import time

@pytest.mark.buttons
def test_new_user_registration_and_password_setup(driver):

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
    
    time.sleep(3)
    assert home.is_on_home_page(), "The site should be on home page after login"
    home.close_promotion_banner()

    assert home.get_logged_email() == temporary_email, f"Logged email should be {temporary_email}, but it is {home.get_logged_email()}"
    home.go_to_my_account()

    myAccount = MyAccount(driver)
    #assert myAccount.is_on_my_account_page(), "The site should be on My Account page"

    time.sleep(5)
    myAccount.click_on_register()
    #time.sleep(30)

# 1. Access the website: Open the browser and go to the Americanas website.
# 2. Navigate to Registration: Click on the "Login or Sign Up" option.
# 3. Generate Temporary Email: In a new tab, go to https://temp-mail.io/ and copy the generated email.
# 4. Enter Email: Return to the Americanas website, enter the temporary email in the registration field, and click to send the verification code.
# 5. Get Code: Go back to the temp-mail website, open the received email, and copy the verification code.
# 6. Confirm Registration: Return to the Americanas website and enter the code to finalize the registration.
# 7. Verify Redirect: Confirm that you have been redirected to the homepage.
# 8. Validate Login: Check if the new user's email is displayed in the page header.

# 9. Access My Account: Open the "My Account" menu and confirm that the email in the registration tab is correct.
# 10. Start Password Setup: Navigate to the authentication section and select "Set Password".
# 11. Enter Password Code: Get the new code sent to temp-mail and enter it in the corresponding field.
# 12. Test Password Rules:
    # Try to save a password with less than 8 characters. The "Save" button should be inactive.
    # Try to save a password without numbers. The "Save" button should be inactive.
    # Try to save a password without lowercase letters. The "Save" button should be inactive.
    # Try to save a password without uppercase letters. The "Save" button should be inactive.
# 13. Set Valid Password: Enter a password that meets all criteria and click "Save Password".
# 14. Validate success: Validate that the password was saved successfully (just validate that the sequence of asterisks appeared on the screen).