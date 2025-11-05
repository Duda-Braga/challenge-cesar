import pytest
import time
import json
from pages.home_page import Home
from pages.search_page import Search
from pages.product_page import Product

import json
from pathlib import Path
import os

def load_wishlist():
    """Reads the JSON from data and returns it as a dictionary"""
    json_path = Path(__file__).parent.parent / "data" / "generated_wishlist_fixture.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

@pytest.mark.parametrize("data_set",  load_wishlist())
def test_product_purchase_flow(driver, data_set):

    product_price = data_set['Price']
    product_name = data_set['Product']
    product_delivery = data_set['delivery_estimate']
    product_zipcode = data_set['Zipcode']
    product_shippingfee = data_set['shipping_fee']


    home = Home(driver)
    assert home.is_on_home_screen(), "App did not launch correctly"

    home.go_to_serach_page()
    search = Search(driver)
    search.search_element(product_name)
    assert search.click_on_first_product(), "ERROR: couldt not find the product"

    product = Product(driver)
    assert product.is_product_name_correct(product_name), "Name is not correspoding according to the API response"
    assert product.is_product_price_correct(product_price), "Price is not correspoding according to the API response"
    
    product.find_zip_field()
    product.fill_invalid_zip_code()
    assert product.is_error_message_on_screen(), "The error message did not appear when entering the incorrect zip code"
    product.clear_zip_code_field()
    product.fill_valid_zip_code(product_zipcode)
    assert product.is_delivery_time_on_screen(), "The delivery time should appear when entering a correct zip code"
    
    assert product.get_delivery_time() == product_delivery, f"Delivery time is not correspoding according to the API response. It shpuld be {product_delivery}, but it is {product.get_delivery_time()}"
    assert product.get_shipping_cost() == product_shippingfee, f"Shipping cost is not correspoding according to the API response. It shpuld be {product_shippingfee}, but it is {product.get_shipping_cost()}"

    product.click_on_buy_product()
    time.sleep(3)

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