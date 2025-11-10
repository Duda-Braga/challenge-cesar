import pytest
from pages.home_page import Home
from pages.search_page import Search
from pages.productView_page import ProductView
from pages.product_page import Product

@pytest.mark.mobile_test
def test_search_view_product(driver, data_set):

    product_price = data_set['Price']
    product_name = data_set['Product']

    home = Home(driver)
    assert home.is_on_home_screen(), "App did not launch correctly"

    home.go_to_search_page()
    search = Search(driver)
    search.search_element_enter(product_name)

    productView = ProductView(driver)
    assert productView.is_product_name_correct(product_name), "Could not find the product with that corresponding name in Grid View"
    assert productView.is_product_price_correct(product_name, product_price), "Price is not correspoding according to the API response in Grid View"

    assert productView.change_type_of_visualization(), "Error to change type os visualization"
    assert productView.is_product_name_correct(product_name), "Could not find the product with that corresponding name in List View"
    assert productView.is_product_price_correct(product_name, product_price), "Price is not correspoding according to the API response in List View"

    productView.click_product(product_name)

    product = Product(driver)
    assert product.is_product_name_correct(product_name), "Name is not correspoding according to the API response"
    assert product.is_product_price_correct(product_price), "Price is not correspoding according to the API response"

    product.go_to_product_detail()
    