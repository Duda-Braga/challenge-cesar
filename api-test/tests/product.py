import pytest
import uuid 

PRODUCT_TEST_A_unique_id = str(uuid.uuid4()) 
PRODUCT_TEST_A_email = f"testA_{PRODUCT_TEST_A_unique_id}@example.com"
PRODUCT_TEST_A_username = f"userA_{PRODUCT_TEST_A_unique_id[:8]}"
PRODUCT_TEST_A_password = "testA_password"
PRODUCT_TEST_A_id = None
PRODUCST_TEST_A_wishlist_id = None
PRODUCT_TEST_A_auth = None

PRODUCT_TEST_B_unique_id = str(uuid.uuid4()) 
PRODUCT_TEST_B_email = f"testB_{PRODUCT_TEST_B_unique_id}@example.com"
PRODUCT_TEST_B_username = f"userB_{PRODUCT_TEST_B_unique_id[:8]}"
PRODUCT_TEST_B_password = "testB_password"
PRODUCT_TEST_B_id = None
PRODUCT_TEST_B_auth = None

@pytest.mark.api_test
@pytest.mark.product_test
def test_authenticated_user_A(base_url, api_client):
    """"single registration for all post product tests"""
    
    
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


    # login
    login_data = {
        "email": PRODUCT_TEST_A_email,
        "password": PRODUCT_TEST_A_password, 
    }

    login_response =  api_client.post(f"{base_url}/auth/login", json=login_data)
    assert login_response.status_code == 200, f"Status should be 200 for correct login, but it is {login_response.status_code}"

    data_login = login_response.json()
    auth_headers = {"Authorization": f"Bearer {data_login['access_token']}"}
    global PRODUCT_TEST_A_auth 
    PRODUCT_TEST_A_auth = auth_headers

    # create wishlist and producst
    unique_id = str(uuid.uuid4()) 
    wish_name = f"Wishlist name {unique_id}"
    wish_data = {"name": wish_name}

    wish_response = api_client.post(f"{base_url}//wishlists", json=wish_data, headers=auth_headers)
    assert wish_response.status_code == 200, f"Status should be 200 for create new wishlist, but it is {wish_response.status_code}"

    data_wishilist = wish_response.json()
    wishilist_id = data_wishilist.get('id')
    global PRODUCST_TEST_A_wishlist_id
    PRODUCST_TEST_A_wishlist_id = wishilist_id

    product_data_1 = {
        "Price": "10,2235.99",
        "Product": "Apple iPhone",
        "Zipcode": "90212",
        "delivery_estimate": "9 days",
        "shipping_fee": "10.00"
    }

    product_data_2 = {
        "Price": "3,118.99",
        "Product": "iPhone 2",
        "Zipcode": "32212",
        "delivery_estimate": "3 days",
        "shipping_fee": "100.00"
    }

    product_data_3 = {
        "Price": "987.99",
        "Product": "Pirate iPhone",
        "Zipcode": "54672",
        "delivery_estimate": "1 days",
        "shipping_fee": "2.00"
    }

    product_response = api_client.post(f"{base_url}/wishlists/{wishilist_id}/products", json=product_data_1, headers=auth_headers)
    assert product_response.status_code == 200, f"Status should be 200 for adding a product on wishlist, but it is {product_response.status_code}"

    product_response = api_client.post(f"{base_url}/wishlists/{wishilist_id}/products", json=product_data_2, headers=auth_headers)
    assert product_response.status_code == 200, f"Status should be 200 for adding a product on wishlist, but it is {product_response.status_code}"
    
    product_response = api_client.post(f"{base_url}/wishlists/{wishilist_id}/products", json=product_data_3, headers=auth_headers)
    assert product_response.status_code == 200, f"Status should be 200 for adding a product on wishlist, but it is {product_response.status_code}"


@pytest.mark.api_test
@pytest.mark.product_test
def test_authenticated_user_B(base_url, api_client):
    """"single registration for all post product tests, user B"""
    
    
    user_data = {
        "email": PRODUCT_TEST_B_email,
        "password": PRODUCT_TEST_B_password, 
        "username": PRODUCT_TEST_B_username
    }
    
    response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200, f"Status should be 200 for correct registration, but it is {response.status_code}"

    data = response.json()
    global PRODUCT_TEST_B_id
    PRODUCT_TEST_B_id = data.get("id")

    # login
    login_data_B = {
        "email": PRODUCT_TEST_B_email,
        "password": PRODUCT_TEST_B_password, 
    }
    login_response_B =  api_client.post(f"{base_url}/auth/login", json=login_data_B)
    assert login_response_B.status_code == 200, f"Status should be 200 for correct login, but it is {login_response_B.status_code}"

    data_login_B = login_response_B.json()
    auth_headers_B = {"Authorization": f"Bearer {data_login_B['access_token']}"}
    global PRODUCT_TEST_B_auth 
    PRODUCT_TEST_B_auth = auth_headers_B



#post

@pytest.mark.api_test
@pytest.mark.product_test
def test_successfully_add_product_to_wishlist(base_url, api_client):

    product_data = {
        "Price": "15.99",
        "Product": "The Great Gatsby",
        "Zipcode": "90210",
        "delivery_estimate": "5 days",
        "shipping_fee": "2.00"
    }

    product_response = api_client.post(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products", json=product_data, headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 200, f"Status should be 200 for adding a product on wishlist, but it is {product_response.status_code}"

    data_product = product_response.json()
    assert 'id' in data_product,  "Product ID is missing in the  response body"
    assert 'wishlist_id' in data_product, "Wishilist ID is missing in the  response body"
    assert data_product.get('wishlist_id') == PRODUCST_TEST_A_wishlist_id, f"Product should be {PRODUCST_TEST_A_wishlist_id}, but it is {data_product.get('wishilist_id')}"
    assert data_product.get('Product') == product_data['Product'], f"Product should be {product_data['Product']}, but it is {data_product.get('Product')}"
    assert data_product.get('is_purchased') == False, "is_purchased field should be false"


@pytest.mark.api_test
@pytest.mark.product_test
def test_add_product_to_nonexistent_wishlist(base_url, api_client):
    product_data = {
        "Price": "15.99",
        "Product": "The Great Gatsby",
        "Zipcode": "90210",
        "delivery_estimate": "5 days",
        "shipping_fee": "2.00"
    }

    product_response = api_client.post(f"{base_url}/wishlists/999999/products", json=product_data, headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 404, f"Status should be 404 for adding a product on a non-existing wishlist, but it is {product_response.status_code}"
    
    data_product = product_response.json()
    expected_error_msg = 'Wishlist not found'
    error_msg =  data_product.get("detail")
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for unathenticated user, but it it {error_msg}"

@pytest.mark.api_test
@pytest.mark.product_test
def test_add_product_anothers_users_wishilist(base_url, api_client):
    product_data = {
        "Price": "15.99",
        "Product": "The Great Gatsby",
        "Zipcode": "90210",
        "delivery_estimate": "5 days",
        "shipping_fee": "2.00"
    }

    product_response = api_client.post(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products", json=product_data, headers=PRODUCT_TEST_B_auth)
    assert product_response.status_code == 404, f"Status should be 404 for adding a product on another user wishlist, but it is {product_response.status_code}"
    
    data_product = product_response.json()
    expected_error_msg = 'Wishlist not found'
    error_msg =  data_product.get("detail")
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for unathenticated user, but it it {error_msg}"


@pytest.mark.api_test
@pytest.mark.product_test
def test_add_product_with_incomplete_data(base_url, api_client):
    product_data = {
        "Price": "15.99"
    }

    product_response = api_client.post(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products", json=product_data, headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 422, f"Status should be 422 for adding a product with incloplete data on wishlist, but it is {product_response.status_code}"

    data_product = product_response.json()
    expected_error_msg = 'Missing product data'
    error_msg =  data_product.get("detail")
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for unathenticated user, but it it {error_msg}"



#get
@pytest.mark.api_test
@pytest.mark.product_test
def test_retrieve_product_from_wishlist(base_url, api_client):
    product_response = api_client.get(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products", headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 200,f"Status should be 200 for retriving specifc product from wishlist, but it is {product_response.status_code}"
    data = product_response.json()
    for prod in data:
        assert prod.get('wishlist_id') == PRODUCST_TEST_A_wishlist_id, f"Products should belong to wishlist {PRODUCST_TEST_A_wishlist_id}, but it belongs to {prod.get('wishlist_id')}"


@pytest.mark.api_test
@pytest.mark.product_test
def test_retrieve_especific_product_from_wishlist(base_url, api_client):
    filter = "iPhone"
    product_response = api_client.get(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products?Product={filter}", headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 200,f"Status should be 200 for retriving specifc product from wishlist, but it is {product_response.status_code}"

    data = product_response.json()
    for prod in data:
        assert filter in prod.get('Product'), f"Response body should only contain products whose name contains {filter}, but {prod.get('Product')} dos not have"


@pytest.mark.api_test
@pytest.mark.product_test
def test_retrieve_purchased_product_from_wishlist(base_url, api_client):
    product_response = api_client.get(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products?is_purchased=true", headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 200,f"Status should be 200 for retriving specifc product from wishlist, but it is {product_response.status_code}"

    data = product_response.json()
    for prod in data:
        assert prod.get('is_purchased') != False, f"Response body should only purchased products, but {prod.get('Product')} dos was not"


@pytest.mark.api_test
@pytest.mark.product_test
def test_add_product_anothers_users_wishilist(base_url, api_client):
    product_response = api_client.get(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products", headers=PRODUCT_TEST_B_auth)
    assert product_response.status_code == 404,f"Status should be 404 for retriving products from anothers user wishlist, but it is {product_response.status_code}"
   



#put
@pytest.mark.api_test
@pytest.mark.product_test
def test_update_product(base_url, api_client):
    product_response = api_client.get(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products", headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 200,f"Status should be 200 for retriving specifc product from wishlist, but it is {product_response.status_code}"
    data_product = product_response.json()
    product_id = data_product[0].get('id')

    product_data_update = {
        "Price": "15.000.99"
    }

    product_response_update = api_client.put(f"{base_url}/products/{product_id}" ,json=product_data_update, headers=PRODUCT_TEST_A_auth)
    assert product_response_update.status_code == 200,f"Status should be 200 for updating specifc product from wishlist, but it is {product_response_update.status_code}"

    data_update = product_response_update.json()
    assert data_update.get('Price') == product_data_update['Price'], f"Failed to update, it should be { product_data_update['Price']}, but it it {data_update.get('Price')}"


@pytest.mark.api_test
@pytest.mark.product_test
def test_update_nonexisting_product(base_url, api_client):
    product_data_update = {
        "Price": "13.432.99"
    }

    product_response_update = api_client.put(f"{base_url}/products/9999999" ,json=product_data_update, headers=PRODUCT_TEST_A_auth)
    assert product_response_update.status_code == 404,f"Status should be 404 for updating non existing product from wishlist, but it is {product_response_update.status_code}"


@pytest.mark.api_test
@pytest.mark.product_test
def x(base_url, api_client):
    product_response = api_client.get(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products", headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 200,f"Status should be 200 for retriving specifc product from wishlist, but it is {product_response.status_code}"
    data_product = product_response.json()
    product_id = data_product[0].get('id')

    product_data_update = {
        "Price": "12.297.99"
    }

    product_response_update = api_client.put(f"{base_url}/products/{product_id}" ,json=product_data_update, headers=PRODUCT_TEST_B_auth)
    assert product_response_update.status_code == 404,f"Status should be 404 for updating anothers user product, but it is {product_response_update.status_code}"




#delete
@pytest.mark.api_test
@pytest.mark.product_test
def test_delete_product(base_url, api_client):
    product_response = api_client.get(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products", headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 200,f"Status should be 200 for retriving specifc product from wishlist, but it is {product_response.status_code}"
    data_product = product_response.json()
    product_id = data_product[-1].get('id')

    product_response_update = api_client.delete(f"{base_url}/products/{product_id}", headers=PRODUCT_TEST_A_auth)
    assert product_response_update.status_code == 204,f"Status should be 204 for deleting specifc product from wishlist, but it is {product_response_update.status_code}"

@pytest.mark.api_test
@pytest.mark.product_test
def test_delete_nonexistent_product(base_url, api_client):
    product_response_update = api_client.delete(f"{base_url}/products/999999", headers=PRODUCT_TEST_A_auth)
    assert product_response_update.status_code == 404,f"Status should be 404 for deleting a non-existent product, but it is {product_response_update.status_code}"

@pytest.mark.api_test
@pytest.mark.product_test
def test_delete_another_user_product(base_url, api_client):
    product_response = api_client.get(f"{base_url}/wishlists/{PRODUCST_TEST_A_wishlist_id}/products", headers=PRODUCT_TEST_A_auth)
    assert product_response.status_code == 200,f"Status should be 200 for retriving specifc product from wishlist, but it is {product_response.status_code}"
    data_product = product_response.json()
    product_id = data_product[-1].get('id')

    product_response_update = api_client.delete(f"{base_url}/products/{product_id}", headers=PRODUCT_TEST_B_auth)
    assert product_response_update.status_code == 404,f"Status should be 404 for deleting anothers user product, but it is {product_response_update.status_code}"
