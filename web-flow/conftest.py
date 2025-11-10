import pytest
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
import datetime 
from setup_fixture import get_products_and_save_json

JSON_FILENAME = "test_generated_wishlist_fixture.json"

def pytest_generate_tests(metafunc):
    if "data_set" not in metafunc.fixturenames:
        return

    try:
        get_products_and_save_json() 
    except Exception as e:
        raise RuntimeError(f"Failed to update JSON in pytest_generate_tests: {e}") from e

    json_path = Path(__file__).parent / JSON_FILENAME
    if not json_path.exists():
        raise RuntimeError(f"JSON file not found after update: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def make_id(item, idx):
        if isinstance(item, dict) and "sku" in item:
            return f"{idx}-{item.get('sku')}"
        return f"case-{idx}"

    ids = [make_id(item, i) for i, item in enumerate(data)]
    metafunc.parametrize("data_set", data, ids=ids)



# defines the --browser command-line option
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to execute tests (chrome or firefox)")

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    
    if browser == "chrome":
        options = ChromeOptions()
        # suppress the browser's native notification pop-up
        options.add_argument("--disable-notifications") 
        driver_instance = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()), options=options)
        # driver_instance = webdriver.Chrome(options=options)
        
    elif browser == "firefox":
        driver_instance = webdriver.Firefox()
    else:
        raise ValueError(f"Browser '{browser}' is not supported")
    
    driver_instance.maximize_window()
    
    # Stores the browser in the request for future hook use (optional, but good for reporting)
    request.node.browser = browser 
    
    # The 'yield' hands over the driver to the test and pauses the fixture.
    yield driver_instance
    
    # Cleanup: Ensures the driver is closed after the test.
    driver_instance.quit()

@pytest.fixture(scope="session")
def load_data():
    """Reads the data JSON and returns it as a dictionary"""
    json_path = Path(__file__).parent / "data" / "test_data.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        if rep.failed and "driver" in item.fixturenames:
            
            driver = item.funcargs["driver"]
            
            # Ensures the directory exists
            screenshot_dir = Path(__file__).parent / "error_screenshot" 
            screenshot_dir.mkdir(parents=True, exist_ok=True) 
            
            # Generating unique timestamp for the file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = screenshot_dir / f"{timestamp}_screenshot_{item.name}.png"
            
            try:
                # Selenium uses get_screenshot_as_file method
                driver.get_screenshot_as_file(screenshot_name)
                print(f"\nScreenshot saved as {screenshot_name}")
            except Exception as e:
                # Handle error if screenshot fails
                print(f"\nWARNING: Failed to save screenshot: {e}")