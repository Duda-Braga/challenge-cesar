import pytest
import uuid 

PRODUCT_TEST_A_unique_id = str(uuid.uuid4()) 
PRODUCT_TEST_A_email = f"testA_{PRODUCT_TEST_A_unique_id}@example.com"
PRODUCT_TEST_A_username = f"userA_{PRODUCT_TEST_A_unique_id[:8]}"
PRODUCT_TEST_A_password = "testA_password"
PRODUCT_TEST_A_id = None

@pytest.mark.api_test
@pytest.mark.product_test
def test_authenticated_user_A(base_url, api_client):
    """"single registration for all product tests"""
    
    
    user_data = {
        "email": PRODUCT_TEST_A_email,
        "password": PRODUCT_TEST_A_password, 
        "username": PRODUCT_TEST_A_username
    }
    
    response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200, f"Status should be 200 for correct registration, but it is {response.status_code}"

    data = response.json()
    global PRODUCT_TEST_A_id
    PRODUCT_TEST_A_id = data.get("id")







@pytest.mark.api_test
@pytest.mark.product_test
def test_successfully_add_product_to_wishlist(base_url, api_client):
    login_data = {
        "email": PRODUCT_TEST_A_email,
        "password": PRODUCT_TEST_A_password, 
    }
    login_response =  api_client.post(f"{base_url}/auth/login", json=login_data)
    assert login_response.status_code == 200, f"Status should be 200 for correct login, but it is {login_response.status_code}"

    data_login = login_response.json()
    auth_headers = {"Authorization": f"Bearer {data_login['access_token']}"}


    unique_id = str(uuid.uuid4()) 
    wish_name = f"Wishlist name {unique_id}"
    wish_data = {"name": wish_name}

    wish_response = api_client.post(f"{base_url}//wishlists", json=wish_data, headers=auth_headers)
    assert wish_response.status_code == 200, f"Status should be 200 for create new wishlist, but it is {wish_response.status_code}"

    data_wishilist = wish_response.json()
    wishilist_id = data_wishilist.get('id')

    product_data = {
    "Price": "15.99",
    "Product": "The Great Gatsby",
    "Zipcode": "90210",
    "delivery_estimate": "5 days",
    "shipping_fee": "2.00"
    }

    product_response = api_client.post(f"{base_url}/wishlists/{wishilist_id}/products", json=product_data, headers=auth_headers)
    assert product_response.status_code == 200, f"Status should be 200 for adding a product on wishlist, but it is {product_response.status_code}"

    data_product = product_response.json()
    assert 'id' in data_product,  "Product ID is missing in the  response body"
    assert 'wishlist_id' in data_product, "Wishilist ID is missing in the  response body"
    assert data_product.get('wishlist_id') == wishilist_id, f"Product should be {wishilist_id}, but it is {data_product.get('wishilist_id')}"
    assert data_product.get('Product') == product_data['Product'], f"Product should be {product_data['Product']}, but it is {data_product.get('Product')}"
    assert data_product.get('is_purchased') == False, "is_purchased field should be false"


@pytest.mark.api_test
@pytest.mark.product_test
def test_add_product_to_nonexistent_wishlist(base_url, api_client):
    login_data = {
        "email": PRODUCT_TEST_A_email,
        "password": PRODUCT_TEST_A_password, 
    }
    login_response =  api_client.post(f"{base_url}/auth/login", json=login_data)
    assert login_response.status_code == 200, f"Status should be 200 for correct login, but it is {login_response.status_code}"

    data_login = login_response.json()
    auth_headers = {"Authorization": f"Bearer {data_login['access_token']}"}


    product_data = {
    "Price": "15.99",
    "Product": "The Great Gatsby",
    "Zipcode": "90210",
    "delivery_estimate": "5 days",
    "shipping_fee": "2.00"
    }

    product_response = api_client.post(f"{base_url}/wishlists/99999/products", json=product_data, headers=auth_headers)
    assert product_response.status_code == 404, f"Status should be 404 for adding a product on a non-existing wishlist, but it is {product_response.status_code}"
    
    data_product = product_response.json()
    expected_error_msg = 'Wishlist not found'
    error_msg =  data_product.get("detail")
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for unathenticated user, but it it {error_msg}"

