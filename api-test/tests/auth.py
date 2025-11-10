import pytest
import requests
import uuid 

@pytest.mark.api_test
@pytest.mark.authentication_test
@pytest.mark.post
def test_susscefull_user_registration(base_url, api_client):
    unique_id = str(uuid.uuid4()) # generates a unique identifier
    new_email = f"test_{unique_id}@example.com"
    new_username = f"user_{unique_id[:8]}"

    user_data = {
        "email": new_email,
        "password": "password123", 
        "username": new_username
    }
    
    response = api_client.post(f"{base_url}/auth/register", json=user_data)

    assert response.status_code == 200, f"Status should be 200, but it is {response.status_code}"
    data = response.json()
    assert "id" in data, "User ID is missing in the registration response"
    assert data.get("email") == user_data["email"], f"Returned email {data.get('email')} does not match the sent email {user_data['email']}" 
    assert "password" not in data, "Password should not be returned in the response body"


@pytest.mark.api_test
@pytest.mark.authentication_test
@pytest.mark.post
def test_registration_existing_email(base_url, api_client):
    # valid registration
    unique_id = str(uuid.uuid4())
    email = f"{unique_id}@existing.com"
    username = f"user_{unique_id[:8]}"

    user_data = {
        "email": email,
        "password": "password123", 
        "username": username
    }

    initial_response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert initial_response.status_code == 200, f"Status should be 200 for first registration, but it is {initial_response.status_code}"

    # duplicated register
    duplicate_user_data = {
        "email": email,
        "password": "anotherpassword", 
        "username": f"new_{str(uuid.uuid4())[:8]}" 
    }

    duplicate_response = api_client.post(f"{base_url}/auth/register", json=duplicate_user_data)
    assert duplicate_response.status_code == 400, f"Status should be 400 for duplicated email registration, but it is {duplicate_response.status_code}"
    
    data = duplicate_response.json()
    expected_error_message = "Email already registered"

    error_detail = data.get("detail", duplicate_response.text)
    assert expected_error_message in error_detail, f"Expected error message '{expected_error_message}' not found in response body: {error_detail}"

@pytest.mark.api_test
@pytest.mark.authentication_test
@pytest.mark.post
def test_registration_invalid_email_format(base_url, api_client):

    unique_id = str(uuid.uuid4())
    username = f"any_user_{unique_id[:8]}"

    user_data = {
        "email": "not-an-email",
        "password": "password123", 
        "username": username
    }

    email_error_response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert email_error_response.status_code == 422, f"Status should be 422 for invalid email registration, but it is {email_error_response.status_code}" 

    data_email_error = email_error_response.json()
    error_msg = data_email_error.get("detail")
    expected_error_msg = "Invalid email format"
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for invalid email format registrarion, but it it {error_msg}"

@pytest.mark.api_test
@pytest.mark.authentication_test
@pytest.mark.post
def test_registration_invalid_email_format(base_url, api_client):

    unique_id = str(uuid.uuid4())
    username = f"any_user_{unique_id[:8]}"

    user_data = {
        "email": "not-an-email",
        "password": "password123", 
        "username": username
    }

    email_error_response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert email_error_response.status_code == 422, f"Status should be 422 for invalid email registration, but it is {email_error_response.status_code}" 

    data_email_error = email_error_response.json()
    error_msg = data_email_error.get("detail")
    expected_error_msg = "Invalid email format"
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for invalid email format registrarion, but it it {error_msg}"

@pytest.mark.api_test
@pytest.mark.authentication_test
@pytest.mark.post
def test_registration_empty_password(base_url, api_client):

    unique_id = str(uuid.uuid4())
    email = f"test_{unique_id}@example.com"
    username = f"user_{unique_id[:8]}"

    user_data = {
        "email": email,
        "password": "", 
        "username": username
    }

    password_error_response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert password_error_response.status_code == 422, f"Status should be 422 for empty password registration, but it is {password_error_response.status_code}" 

    data_password_error = password_error_response.json()
    error_msg = data_password_error.get("detail")
    expected_error_msg = "Missing data"
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for registrarion without a password field, but it it {error_msg}"


LOGIN_TEST_unique_id = str(uuid.uuid4()) 
LOGIN_TEST_email = f"test_{LOGIN_TEST_unique_id}@example.com"
LOGIN_TEST_username = f"user_{LOGIN_TEST_unique_id[:8]}"
LOGIN_TEST_password = "correct_password"

@pytest.mark.api_test
@pytest.mark.authentication_test
@pytest.mark.post
def test_new_user(base_url, api_client):
    """"single registration for all login tests"""
    
    user_data = {
        "email": LOGIN_TEST_email,
        "password": LOGIN_TEST_password, 
        "username": LOGIN_TEST_username
    }
    
    response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200, f"Status should be 200 for correct registration, but it is {response.status_code}"


@pytest.mark.api_test
@pytest.mark.authentication_test
@pytest.mark.post
def test_succesful_login(base_url, api_client):

    login_data = {
        "email": LOGIN_TEST_email,
        "password": LOGIN_TEST_password
    }

    login_response = api_client.post(f"{base_url}/auth/login", json=login_data)
    assert login_response.status_code == 200, f"Status should be 200 for successful login, but it is {login_response.status_code}"

    data_login = login_response.json()
    assert "access_token" in data_login, "Access token is missing in the login response"
    assert data_login.get("token_type") == "bearer", f"Token type should be bearer, but it is {data_login.get('token_type')}"
    

@pytest.mark.api_test
@pytest.mark.authentication_test
@pytest.mark.post
def test_login_wrong_password(base_url, api_client):

    login_data = {
        "email": LOGIN_TEST_email,
        "password": "wrong_password"
    }

    login_response = api_client.post(f"{base_url}/auth/login", json=login_data)
    assert login_response.status_code == 401, f"Status should be 401 (unauthorized) for login with incorrect password, but it is {login_response.status_code}"

    data_login = login_response.json()
    error_msg = data_login.get("detail")
    expected_error_msg = "Incorrect email or password"
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for login with incorrect password, but it it {error_msg}"


@pytest.mark.api_test
@pytest.mark.authentication_test
@pytest.mark.post
def test_login_non_existent_user(base_url, api_client):

    login_data = {
        "email": f"non_existing{LOGIN_TEST_email}",
        "password": LOGIN_TEST_password
    }

    login_response = api_client.post(f"{base_url}/auth/login", json=login_data)
    assert login_response.status_code == 401, f"Status should be 401 (unauthorized) for login with Non-Existent User, but it is {login_response.status_code}"

    data_login = login_response.json()
    error_msg = data_login.get("detail")
    expected_error_msg = "Incorrect email or password"
    assert error_msg == expected_error_msg, f"Error message should be {expected_error_msg} for login with Non-Existent User, but it it {error_msg}"


