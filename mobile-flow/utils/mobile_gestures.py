from appium.webdriver.webdriver import WebDriver

class MobileGestures:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def scroll_screen(self, direction: str, percent: float = 1.0):
        """
        Scroll gesture on the screen in the specified direction

        Args:
            direction (str): The scroll direction ("up" or "down").
            percent (float): The force/distance of the scroll (default 1.0).
        """
        # Ensure the direction is valid
        if direction.lower() not in ["up", "down"]:
            raise ValueError("The direction must be 'up' or 'down'.")
            
        size = self.driver.get_window_size()
        screen_width = size['width']
        screen_height = size['height']

        # Defines the scroll coordinates (a centered point)
        # Starts the touch at 30% of the height, moves 50% of the screen height.
        self.driver.execute_script("mobile: scrollGesture", {
            "left": 0,
            "top": screen_height * 0.3, 
            "width": screen_width,
            "height": screen_height * 0.5, 
            "direction": direction.lower(), # Uses the parameter here
            "percent": percent
        })

   
