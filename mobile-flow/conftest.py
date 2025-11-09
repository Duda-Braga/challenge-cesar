import pytest
import json
import base64
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



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Executes the test and obtains the report object.
    outcome = yield
    rep = outcome.get_result()

    # We use the 'call' stage because it contains the assert result.
    if rep.when == "call":
        # 1. ATTACH THE REPORT (ESSENTIAL FOR CONDITIONAL VIDEO SAVING IN TEARDOWN)
        item.rep_call = rep
        
        # 2. SCREENSHOT LOGIC: Save screenshot immediately on failure
        if rep.failed and "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            
            # Ensures the directory exists
            screenshot_dir = Path(__file__).parent / "error_screenshot" 
            screenshot_dir.mkdir(parents=True, exist_ok=True) 
            screenshot_name = screenshot_dir / f"screenshot_{item.name}.png"
            
            try:
                driver.get_screenshot_as_file(screenshot_name)
                print(f"\nScreenshot saved as {screenshot_name}")
            except Exception as e:
                # Handle error if screenshot fails (e.g., driver quits too early)
                print(f"\nWARNING: Failed to save screenshot: {e}")

@pytest.fixture(scope="session")
def load_data():
    """Reads the data JSON and returns it as a dictionary"""
    json_path = Path(__file__).parent / "data" / "test_data.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

@pytest.fixture(scope="function")
def driver(request):
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
        "appium:autoGrantPermissions": True,
        

        # Capabilities for screenshot and video recording
        "appium:androidScreenshotOnFai": True, 
        "appium:nativeWebScreenshot": True,
        "appium:recordVideo": "true", # Enable video recording
        "appium:videoType": "mpeg4"  # Specify video format
     })
    
    _driver = None
    try:
        _driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        _driver.start_recording_screen() 
    except Exception as e:
        pytest.skip(f"Failed to create Appium driver: {e}")
    
    # Yield control to the test function
    yield _driver

    # --- TEARDOWN PHASE ---
    # This code runs AFTER the test function completes (or fails)
    if _driver:
        video_data = None
        try:
            # Stop recording and get the video data (base64 encoded)
            video_data = _driver.stop_recording_screen()
        except Exception as e:
             print(f"\nWARNING: Failed to stop screen recording: {e}")


        test_node = request.node
        # Checks if 'rep_call' was attached AND if the test failed.
        is_failed = getattr(test_node, "rep_call", None) and test_node.rep_call.failed

        if is_failed and video_data:
            # Ensures the directory exists
            video_dir = Path(__file__).parent / "error_video"
            video_dir.mkdir(parents=True, exist_ok=True) 
            
            # MODIFIED: Use the full Path object to define the filename
            video_filename = video_dir / f"video_{request.node.name}.mp4"
            
            try:
                # Decode and save the video file
                with open(video_filename, "wb") as f:
                    f.write(base64.b64decode(video_data))
                print(f"Video saved as {video_filename}")
            except Exception as e:
                print(f"\nWARNING: Failed to save video file: {e}")
                
        print("\nQuitting driver...")
        _driver.quit()

