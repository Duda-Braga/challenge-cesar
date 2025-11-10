import pytest
from pages.home_page import Home
from pages.search_page import Search
from pages.product_page import Product
from pages.cartPopup_page import CartPopup
from pages.cart_page import Cart

@pytest.mark.mobile_test
def test_product_purchase_flow(driver, data_set):

    product_price = data_set['Price']
    product_name = data_set['Product']
    product_delivery = data_set['delivery_estimate']
    product_zipcode = data_set['Zipcode']
    product_shippingfee = data_set['shipping_fee']


    home = Home(driver)
    assert home.is_on_home_screen(), "App did not launch correctly"

    home.go_to_search_page()
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
    
    assert product.get_delivery_time() == product_delivery, f"Delivery time is not correspoding according to the API response. It should be {product_delivery}, but it is {product.get_delivery_time()}"
    assert product.get_shipping_cost() == product_shippingfee, f"Shipping cost is not correspoding according to the API response. It should be {product_shippingfee}, but it is {product.get_shipping_cost()}"

    product.click_on_buy_product()

    cartPopup = CartPopup(driver)
    assert cartPopup.is_product_name_correct(product_name),  "Name is not correspoding according to the API response"
    assert cartPopup.is_product_price_correct(product_price), "Price is not correspoding according to the API response"

    increase_target = 2
    decrease_target = 1
    cartPopup.increase_quantity_untill_X(increase_target)
    assert cartPopup.get_product_quantity() == increase_target, f"Quantity field did not updated when incresing qunatity. It should be {increase_target}, but it is {cartPopup.get_product_quantity()}"
    
    cartPopup.decrease_quantity_untill_X(decrease_target)
    assert cartPopup.get_product_quantity() == decrease_target, f"Quantity field did not updated when decrease qunatity. It should be {decrease_target}, but it is {cartPopup.get_product_quantity()}"
    cartPopup.increase_qunatity()
    assert cartPopup.get_product_quantity() > 0; "Decrease button should be inactive"

    cartPopup.increase_quantity_untill_X(increase_target)
    assert cartPopup.get_product_quantity() == increase_target, f"Quantity field did not updated when incresing qunatity. It should be {increase_target}, but it is {cartPopup.get_product_quantity()}"
    
    cartPopup.add_to_cart()
    
    product.go_to_cart()
    cart = Cart(driver)
    assert cart.is_product_name_correct(product_name),  "Name is not correspoding according to the API response"
    assert cart.is_product_quantity_correct(increase_target), "Quantity is not correspoding"
    cart.find_total_price()

    
    # convert to number
    temporary_price = product_price.replace('.', '') 
    price_format = temporary_price.replace(',', '.') 
    product_price_float = float(price_format)

    total_price = product_price_float * increase_target
    assert cart.get_subtotal_price() == total_price, f"Subtotal price is not {increase_target}x bigger than original price. It should be {total_price}, but it is {cart.get_subtotal_price()}"
    assert cart.get_total_price() == total_price, f"Total price is not {increase_target}x bigger than original price. It should be {total_price}, but it is {cart.get_total_price()}"
    assert cart.get_ckecout_price() == total_price, f"Total price on checkout area is not {increase_target}x bigger than original price. It should be {total_price}, but it is {cart.get_total_price()}"
    
    cart.fill_invalid_zip_code()
    assert cart.is_error_message_on_screen(), "The error message did not appear when entering the incorrect zip code"
    cart.clear_zip_code_field()
    cart.fill_valid_zip_code(product_zipcode)
    assert cart.is_delivery_time_on_screen(), "The delivery time should appear when entering a correct zip code"
    
    assert cart.get_delivery_time() == product_delivery, f"Inconsistency. Delivery time is not correspoding according to the API response. It should be {product_delivery}, but it is {product.get_delivery_time()}"
    assert cart.get_shipping_cost() == product_shippingfee, f"Inconsistency. Shipping cost is not correspoding according to the API response. It should be {product_shippingfee}, but it is {product.get_shipping_cost()}"

    cart.proceed_to_checkout()
    assert cart.check_redirection(), "Failed to procced to checkout, login/checkout screen is not displayed"