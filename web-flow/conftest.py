import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

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