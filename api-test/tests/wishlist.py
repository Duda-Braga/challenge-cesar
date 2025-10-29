import pytest
import uuid 

WISH_TEST_unique_id = str(uuid.uuid4()) 
WISH_TEST_email = f"test_{WISH_TEST_unique_id}@example.com"
WISH_TEST_username = f"user_{WISH_TEST_unique_id[:8]}"
WISH_TEST_password = "test_password"

@pytest.mark.api_test
@pytest.mark.wishlist_test
def test_authenticated_user(base_url, api_client):
    """"single registration for all wishilist tests"""
    
    user_data = {
        "email": WISH_TEST_email,
        "password": WISH_TEST_password, 
        "username": WISH_TEST_username
    }
    
    response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200, f"Status should be 200 for correct registration, but it is {response.status_code}"



@pytest.mark.api_test
@pytest.mark.wishlist_test
def test_susscefull_create_wishlsit(base_url, api_client):

    login_data = {
        "email": WISH_TEST_email,
        "password": WISH_TEST_password, 
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
    assert "id" in data_wishilist, "ID wishlist is missing in the Wishlist response body"
    assert data_wishilist.get("name") == wish_data["name"], f"Returned name wishlist {data_wishilist.get('name')} does not match the sent name {wish_data['name']}"
    assert "owner_id" in data_wishilist, "Owner ID is missing in the Wishlist response body"


