import requests
import json
import os
from pathlib import Path

CREDENTIALS = {
  "email": "projeto@example.com",
  "password": "Senha123!",
  "username": "projeto"
}
BASE_URL = "http://127.0.0.1:8000"
DEFAULT_WISHLIST_ID = 1

FILE_NAME = "test_generated_wishlist_fixture.json"


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)) 
OUTPUT_FILE_NAME = os.path.join(SCRIPT_DIR, FILE_NAME)

def get_products_and_save_json():

    client = requests.Session()
    
    #login
    login_url = f"{BASE_URL}/auth/login"
    login_data = {
        "email": CREDENTIALS['email'], 
        "password": CREDENTIALS['password']
    }

    
    login_response =  client.post(login_url, json=login_data)
    assert login_response.status_code == 200, f"Status should be 200 for correct login, but it is {login_response.status_code}"

    data_login = login_response.json()
    auth_header = {"Authorization": f"Bearer {data_login['access_token']}"}


    # get products
    products_url = f"{BASE_URL}/wishlists/{DEFAULT_WISHLIST_ID}/products"
 
    
    products_response = client.get(products_url, headers=auth_header)
    assert products_response.status_code == 200, f"Status should be 200 for correct login, but it is {products_response.status_code}"

    # save as json
    
    api_products_list = products_response.json()
    final_payload = api_products_list
    
    
    with open(OUTPUT_FILE_NAME, 'w', encoding='utf-8') as f:
        # Usa indent=2 para formatar o JSON de forma legível
        json.dump(final_payload, f, ensure_ascii=False, indent=2)
        



# if __name__ == '__main__':
#     get_products_and_save_json()