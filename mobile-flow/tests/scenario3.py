import pytest
import time
from pages.allow_popups_page import Allows #sem fluent pages inicialmente
from pages.home_page import Home
from pages.search_page import Search

def test_product_purchase_flow(driver, load_data):
    #initialize all pages at the beginning for now, fluent pages later
    allowpopup = Allows(driver)
    home = Home(driver)

    allowpopup.allow_all_permitions()

    assert home.is_on_home_screen(), "App did not launch correctly"
    home.go_to_serach_page()

    search = Search(driver)
    search.search_element(load_data)
    time.sleep(10)

# 1. Open App: Launch the Americanas application.
# 2. Search for Product: Use the search bar to look for a product from the wishlist.
# 3. Select Product: Tap on the desired product in the search results.
# 4. Validate Product Page:
# Confirm that the product name and price are correct according to the API response.
# Enter an invalid ZIP code, click "Calculate", and verify that an error message is displayed.
# Enter the valid ZIP code returned by the API and validate the delivery time and shipping cost.
# 5. Add to Cart: Tap the "Buy" button.
# 6. Validate Cart Popup:
# In the cart popup, confirm the product name and price again.
# Increase the quantity to 2 and check if the quantity field is updated.
# Decrease the quantity to 1 and check if the decrease button ( - ) becomes inactive.
# Increase the quantity to 2 again.
# 7. Add and go to cart: Proceed to the cart finalization screen.
# 8. Validate Cart:
# Confirm the product name and quantity.
# Check if the total product value and the order subtotal are double the unit price.
# Confirm that the value on the "Proceed to Checkout" button also reflects the total for two units.
# Repeat the invalid and valid ZIP code test to ensure shipping calculation consistency.
# 9. Proceed to Checkout: Tap "Proceed to Checkout".
# 10. Validate Redirect: Check if the login/checkout screen is displayed with the message "Enter your email to continue".