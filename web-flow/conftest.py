import pytest
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from pathlib import Path

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
        driver_instance = webdriver.Chrome(options=options)
        
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