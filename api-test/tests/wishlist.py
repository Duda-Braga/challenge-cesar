import pytest
import uuid 

WISH_TEST_unique_id = str(uuid.uuid4()) 
WISH_TEST_email = f"test_{WISH_TEST_unique_id}@example.com"
WISH_TEST_username = f"user_{WISH_TEST_unique_id[:8]}"
WISH_TEST_password = "test_password"
WISH_TEST_id = None
WISH_TEST_auth = None

@pytest.mark.api_test
@pytest.mark.wishlist_test
@pytest.mark.post
@pytest.mark.get
def test_authenticated_user(base_url, api_client):
    """"single registration for all wishilist tests"""
    
    user_data = {
        "email": WISH_TEST_email,
        "password": WISH_TEST_password, 
        "username": WISH_TEST_username
    }
    
    response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200, f"Status should be 200 for correct registration, but it is {response.status_code}"

    data = response.json()
    global WISH_TEST_id
    WISH_TEST_id = data.get("id")

    # login
    login_data = {
        "email": WISH_TEST_email,
        "password": WISH_TEST_password, 
    }

    login_response =  api_client.post(f"{base_url}/auth/login", json=login_data)
    assert login_response.status_code == 200, f"Status should be 200 for correct login, but it is {login_response.status_code}"

    data_login = login_response.json()
    auth_headers = {"Authorization": f"Bearer {data_login['access_token']}"}
    global WISH_TEST_auth 
    WISH_TEST_auth = auth_headers


#post wishlist

@pytest.mark.api_test
@pytest.mark.wishlist_test
@pytest.mark.post
def test_susscefull_create_wishlsit(base_url, api_client):
    unique_id = str(uuid.uuid4()) 
    wish_name = f"Wishlist name {unique_id}"
    wish_data = {"name": wish_name}

    wish_response = api_client.post(f"{base_url}//wishlists", json=wish_data, headers=WISH_TEST_auth)
    assert wish_response.status_code == 200, f"Status should be 200 for create new wishlist, but it is {wish_response.status_code}"

    data_wishilist = wish_response.json()
    assert "id" in data_wishilist, "ID wishlist is missing in the Wishlist response body"
    assert data_wishilist.get("name") == wish_data["name"], f"Returned name wishlist {data_wishilist.get('name')} does not match the sent name {wish_data['name']}"
    assert "owner_id" in data_wishilist, "Owner ID is missing in the Wishlist response body"


@pytest.mark.api_test
@pytest.mark.wishlist_test
@pytest.mark.post
def test_duplicate_name_wishlsit(base_url, api_client):
    unique_id = str(uuid.uuid4()) 
    wish_name = f"Wishlist duplicate name {unique_id}"
    wish_data = {"name": wish_name}

    wish_response = api_client.post(f"{base_url}//wishlists", json=wish_data, headers=WISH_TEST_auth)
    assert wish_response.status_code == 200, f"Status should be 200 for create new wishlist, but it is {wish_response.status_code}"

    # same name
    duplicate_response = api_client.post(f"{base_url}//wishlists", json=wish_data, headers=WISH_TEST_auth)
    data_duplicate = duplicate_response.json()
    assert duplicate_response.status_code == 409, f"Status should be 409 (conflict) for create a wishlist with duplicate name, but it is {duplicate_response.status_code}"
    
    expected_error_msg = 'A wishlist with this name already exists'
    error_msg =  data_duplicate.get("message")
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for invalid email format registrarion, but it it {error_msg}"



@pytest.mark.api_test
@pytest.mark.wishlist_test
@pytest.mark.post
def test_create_wishlsit_unauthenticated(base_url, api_client):
    unique_id = str(uuid.uuid4()) 
    wish_name = f"Wishlist duplicate name {unique_id}"
    wish_data = {"name": wish_name}

    wish_response = api_client.post(f"{base_url}//wishlists", json=wish_data)
    assert wish_response.status_code == 401, f"User should not be able to create a wishlist without authentication"

    data_wish = wish_response.json()
    expected_error_msg = 'Not authenticated'
    error_msg =  data_wish.get("detail")
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for unathenticated user, but it it {error_msg}"

    

@pytest.mark.api_test
@pytest.mark.wishlist_test
@pytest.mark.post
def test_create_wishlsit_unauthenticated(base_url, api_client):
    unique_id = str(uuid.uuid4()) 
    wish_name = f"Wishlist duplicate name {unique_id}"
    wish_data = {"name": wish_name}

    wish_response = api_client.post(f"{base_url}//wishlists", json=wish_data)
    assert wish_response.status_code == 401, f"User should not be able to create a wishlist without authentication"

    data_wish = wish_response.json()
    expected_error_msg = 'Not authenticated'
    error_msg =  data_wish.get("detail")
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for unathenticated user, but it is {error_msg}"

    
@pytest.mark.api_test
@pytest.mark.wishlist_test
@pytest.mark.post
def test_create_wishlsit_invalid_data(base_url, api_client):
    wish_data = {"name": ""}

    wish_response = api_client.post(f"{base_url}//wishlists", json=wish_data, headers=WISH_TEST_auth)
    assert wish_response.status_code == 422, f"Status should be 422 for create wishlist with no name, but it is {wish_response.status_code}"

    data_wishilist = wish_response.json()

    expected_error_msg = 'Missing name'
    error_msg = data_wishilist.get("detail")
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for creating a wishlist with invalid data, but it is {error_msg}"




#get wishlist

@pytest.mark.api_test
@pytest.mark.wishlist_test
@pytest.mark.get
def test_successfully_retrieve_all_wishlists(base_url, api_client):
    # assure it has at least one wishlist
    unique_id = str(uuid.uuid4()) 
    wish_name = f"Wishlist name {unique_id}"
    wish_data = {"name": wish_name}

    wish_response = api_client.post(f"{base_url}//wishlists", json=wish_data, headers=WISH_TEST_auth)
    assert wish_response.status_code == 200, f"Status should be 200 for create new wishlist, but it is {wish_response.status_code}"

    get_wish_response = api_client.get(f"{base_url}//wishlists", headers=WISH_TEST_auth)
    assert get_wish_response.status_code == 200, f"Status should be 200 for get wishlist, but it is {get_wish_response.status_code}"
    data_get_wish = get_wish_response.json()
    
    assert len(data_get_wish) > 0, "Wishlist should not be empty"
    for i in range(len(data_get_wish)):
        assert data_get_wish[i].get("owner_id") == WISH_TEST_id, f"Wrong user wishlist, It should be from id_user {WISH_TEST_id}, but it is from {data_get_wish[i].get('owner_id')}"



@pytest.mark.api_test
@pytest.mark.wishlist_test
@pytest.mark.get
def test_retrieve_non_existent_wishlists(base_url, api_client):
    # new user to assure it has an empty wishlist
    new_user_data = {
        "email": f"{WISH_TEST_email}_no_wishlist",
        "password": f"{WISH_TEST_password}_no_wishlist", 
        "username": f"{WISH_TEST_username}_no_wishlist"
    }
    response = api_client.post(f"{base_url}/auth/register", json=new_user_data)
    assert response.status_code == 200, f"Status should be 200 for correct registration, but it is {response.status_code}"

    # login
    new_login_data = {
        "email": f"{WISH_TEST_email}_no_wishlist",
        "password": f"{WISH_TEST_password}_no_wishlist"
    }
    login_response =  api_client.post(f"{base_url}/auth/login", json=new_login_data)
    assert login_response.status_code == 200, f"Status should be 200 for correct login, but it is {login_response.status_code}"

    data_login = login_response.json()
    auth_headers = {"Authorization": f"Bearer {data_login['access_token']}"}

    get_wish_response = api_client.get(f"{base_url}//wishlists", headers=auth_headers)
    assert get_wish_response.status_code == 200, f"Status should be 200 for get empty wishlist, but it is {get_wish_response.status_code}"
    data_get_wish = get_wish_response.json()
    
    assert len(data_get_wish) == 0, "Wishlist should be empty"

@pytest.mark.api_test
@pytest.mark.wishlist_test
@pytest.mark.get
def test_retrieve_wishlists_no_authentication(base_url, api_client):
    # assure it has at least one wishlist
    unique_id = str(uuid.uuid4()) 
    wish_name = f"Wishlist name {unique_id}"
    wish_data = {"name": wish_name}

    wish_response = api_client.post(f"{base_url}//wishlists", json=wish_data, headers=WISH_TEST_auth)
    assert wish_response.status_code == 200, f"Status should be 200 for create new wishlist, but it is {wish_response.status_code}"

    get_wish_response = api_client.get(f"{base_url}//wishlists")
    assert get_wish_response.status_code == 401, f"Status should be 401 for get wishlist unauthorized, but it is {get_wish_response.status_code}"
