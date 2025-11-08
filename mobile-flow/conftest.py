import pytest
import json
from pathlib import Path
from appium import webdriver
from appium.options.common.base import AppiumOptions
from setup_fixture import get_products_and_save_json

JSON_FILENAME = "test_generated_wishlist_fixture.json"

def pytest_generate_tests(metafunc):
    if "data_set" not in metafunc.fixturenames:
        return

    try:
        get_products_and_save_json()
    except Exception as e:
        raise RuntimeError(f"Falha ao atualizar JSON em pytest_generate_tests: {e}") from e

    json_path = Path(__file__).parent / JSON_FILENAME
    if not json_path.exists():
        raise RuntimeError(f"Arquivo JSON não encontrado após atualização: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def make_id(item, idx):
        if isinstance(item, dict) and "sku" in item:
            return f"{idx}-{item.get('sku')}"
        return f"case-{idx}"

    ids = [make_id(item, i) for i, item in enumerate(data)]
    metafunc.parametrize("data_set", data, ids=ids)


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

