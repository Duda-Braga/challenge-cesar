import pytest
import json
from pathlib import Path
from appium import webdriver
from appium.options.common.base import AppiumOptions
from setup_fixture import get_products_and_save_json

# @pytest.fixture(scope="session", autouse=True)
# def update_wishlist_fixture():
#     """
#     Update json with API
#     """
#     try:
#         get_products_and_save_json()
#         print("Fixture JSON successfully generated")
#     except Exception as e:
#         pytest.fail(f"SETUP FAILED: {e}")

#     yield

# @pytest.fixture(scope="session")
def load_wishlist():
    """Reads the JSON from data and returns it as a dictionary"""
    json_path = Path(__file__).parent/ "test_generated_wishlist_fixture.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data



@pytest.fixture(scope="function")
def driver():
    options = AppiumOptions()
    options.load_capabilities({ 
        "platformName": "Android",
        "appium:deviceName": "emulator-5554",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": "com.b2w.americanas",
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:newCommandTimeout": 3600,
        "appium:connectHardwareKeyboard": True,
        "appWaitActivity": "com.b2w.americanas.MainActivity",       
        "appWaitDuration": 60000, 
        "uiautomator2ServerLaunchTimeout": 60000,
        "uiautomator2ServerInstallTimeout": 60000,
        "unicodeKeyboard": False,
        "resetKeyboard": True,
        "appium:autoGrantPermissions": True
     })
    
    _driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    
    yield _driver

    # --- TEARDOWN PHASE ---
    # This code runs AFTER the test function completes (or fails)
    print("\nQuitting driver...")
    _driver.quit()

# @pytest.fixture(scope="module")
# def load_wishlist():
#     """Reads the JSON from data and returns it as a dictionary"""
#     json_path = Path(__file__).parent / "data" / "generated_wishlist_fixture.json"
#     with open(json_path, "r", encoding="utf-8") as f:
#         data = json.load(f)
#     return data

