import pytest
import json
from pathlib import Path
from appium import webdriver
from appium.options.common.base import AppiumOptions

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
        "appWaitDuration": 30000, 
        "uiautomator2ServerLaunchTimeout": 30000,
        "uiautomator2ServerInstallTimeout": 30000,
        "unicodeKeyboard": False,
        "resetKeyboard": True
     })
    
    _driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    
    yield _driver

    # --- TEARDOWN PHASE ---
    # This code runs AFTER the test function completes (or fails)
    print("\nQuitting driver...")
    _driver.quit()